# Release report collector analysis

Date: 2026-10-24 (Asia/Singapore).
Scope: Static inspection of the supplied collector and API wrappers.
The [user request](user-input.md#exact-input) defines this preparation.

**The supplied collector cannot run alone. Missing modules block compilation and prevent exact compliance or coverage reproduction.**

## Observed entry point and data flow

1. `ReleaseReportService.generateReleaseReport(releaseId, tokens?, include?)` resolves its requested sections and ADO token.
2. It connects an ADO client and reads the specified work item.
3. It optionally collects compliance checks, builds, and related work items.
4. Build collection obtains build details, Git comparisons, and optional ADO coverage.
5. Work item collection reads `rtm.json` build attachments and joins their requirement statistics.
6. It returns an object with `release` and the requested sections.

Evidence: [service entry point](../../../core/release-report/release-report.service.ts#L38-L101).

Omitting `include` selects every field from the absent `RELEASE_REPORT_FIELDS` definition.
An empty array requests only the release object.
Build and work item collection run separately.
Requesting work items still reads build attachments when builds are excluded.
Evidence: [section selection](../../../core/release-report/release-report.service.ts#L116-L138), [collection conditions](../../../core/release-report/release-report.service.ts#L63-L89).

The token argument takes precedence over `ADO_TOKEN` when truthy.
Missing tokens throw an error.
The service constructs the client without organization, project, or proxy overrides.
Evidence: [token resolution](../../../core/release-report/release-report.service.ts#L104-L114), [client construction](../../../core/release-report/release-report.service.ts#L49-L54).

## Release identity and custom fields

The input identifies an ADO work item.
The collector does not call the classic Release Management API.
It does not validate the returned work item type.
Evidence: [work item retrieval](../../../core/release-report/ado-api/release.ts#L11-L40).

`Custom.LatestPipelineRuns` and `Custom.DeploymentComponents` supply build references and deployment component labels.
The parser converts HTML to lines and searches for cloud ADO build URLs.
It extracts the numeric `buildId` query value.
It uses the longest matching deployment component prefix when several prefixes match.
Evidence: [release mapping](../../../core/release-report/ado-api/release.ts#L31-L58), [component parsing](../../../core/release-report/ado-api/utils.ts#L70-L126).

Related work items come from `System.LinkTypes.Related`.
The release object also records Tested By relations and `Custom.StoriesLinked`.
The report work item section uses only the Related IDs.
It accepts `Story`, `Generic Task`, `Bug`, and `Subtask` types.
Evidence: [relations](../../../core/release-report/ado-api/release.ts#L59-L76), [type selection](../../../core/release-report/release-report.service.ts#L327-L354).

The release schema declares reviewer approvals, testing scope, change dates, and performance testing documents.
The collector casts its result instead of invoking that schema.
Evidence: [release schema](../../../core/release-report/ado-api/interfaces.ts#L57-L101), [unchecked cast](../../../core/release-report/ado-api/release.ts#L77-L81).

## Observed ADO operations

These operations describe inspected code calls.
They do not establish deployed API compatibility or exact permission scopes.

| Operation | Consumer and evidence | Purpose |
| --- | --- | --- |
| SDK `WebApi.connect` | [client](../../../core/release-report/ado-api/client.ts#L123-L148) | Authenticate with a PAT. |
| SDK `getWorkItems` | [release](../../../core/release-report/ado-api/release.ts#L11-L19) | Read release fields and relations. |
| SDK `getWorkItems` | [work item wrapper](../../../core/release-report/ado-api/workitem.ts#L14-L55) | Read linked work item type and details. |
| `getReleaseComplianceAssessment` | [service](../../../core/release-report/release-report.service.ts#L140-L177) | Collect and normalize compliance gates. Its implementation is absent. |
| SDK `getBuild` | [build wrapper](../../../core/release-report/ado-api/build.ts#L11-L25) | Read build state, repository label, branch, and commit. |
| SDK `getBuildTimeline`, `getAttachment` | [attachment wrapper](../../../core/release-report/ado-api/build.ts#L57-L110) | Read the latest `generatetestreport` task attachment named `rtm.json`. |
| SDK `listPipelines` | [pipeline wrapper](../../../core/release-report/ado-api/pipeline.ts#L10-L21) | Find the first pipeline with a matching name prefix. |
| HTTP POST `/_apis/Contribution/HierarchyQuery/project/{project}?api-version=5.0-preview.1` | [HTTP wrapper](../../../core/release-report/ado-api/extension/HierarchyQuery.ts#L14-L35), [request payload](../../../core/release-report/ado-api/extension/PipelineRuns.ts#L20-L49) | Read UI contribution pipeline runs and stage results. |
| SDK `getBranch`, `getCommitDiffs`, `getCommitsBatch` | [Git wrapper](../../../core/release-report/ado-api/git.ts#L62-L171) | Read branch tips and compare commit histories. |
| `getCoverageSummaryByBuildId`, `getCoverageSummaryByBranchName` | [service](../../../core/release-report/release-report.service.ts#L205-L253), [bindings](../../../core/release-report/ado-api/client.ts#L221-L228) | Read candidate and production coverage. Their implementations are absent. |

## Baseline and coverage rules

The Git checks compare the build commit with its branch tip and production baseline.
For non-main branches, they also compare against `main` and compare `main` against production.
The result removes changed file details from these comparison objects.
Evidence: [comparison orchestration](../../../core/release-report/ado-api/git.ts#L287-L429).

The production baseline uses runs whose `prod` stage has numeric result `0`.
It excludes runs with a `rollback_prod` stage unless its result is `4`.
It sorts qualifying runs by the production stage finish time and selects the first run.
This is the code's inference about production, not independently verified deployment evidence.
Evidence: [stage filtering](../../../core/release-report/ado-api/pipeline.ts#L80-L94), [run sorting](../../../core/release-report/ado-api/pipeline.ts#L140-L174), [baseline selection](../../../core/release-report/ado-api/git.ts#L123-L146).

The search reads release-keyword runs and main-keyword runs.
It requests one additional release page only when the first page has no qualifying production run.
It does not exhaust all pages.
Evidence: [bounded search](../../../core/release-report/ado-api/pipeline.ts#L96-L138), [page size comment](../../../core/release-report/ado-api/extension/PipelineRuns.ts#L4-L19).

Behind-commit exceptions use commit messages beginning with `Merge`.
They do not inspect commit parent counts.
Evidence: [merge-message checks](../../../core/release-report/ado-api/git.ts#L330-L382).

Coverage collection runs only when the branch name contains a digit.
The response must contain numeric `lineCoverage` and `branchCoverage`.
The service maps these values into Sonar-shaped fields.
The active service does not construct or call `SonarQubeClient`.
Evidence: [coverage collection](../../../core/release-report/release-report.service.ts#L205-L253), [eligibility and parsing](../../../core/release-report/release-report.service.ts#L376-L420).

## Test and defect statistics

The build attachment contract selects task `generatetestreport`, type `test.report`, and file `rtm.json`.
The latest matching timeline record wins by finish time.
JSON parsing uses a TypeScript cast, although a `TestReportSchema` exists.
Evidence: [attachment selection](../../../core/release-report/ado-api/build.ts#L69-L107), [JSON cast](../../../core/release-report/release-report.service.ts#L292-L324), [schema](../../../core/release-report/ado-api/interfaces.ts#L440-L480).

The collector flattens requirement coverage from all successful attachment reads.
Each work item receives statistics from the first matching requirement ID.
It does not aggregate multiple build results for the same requirement.
It does not check the attachment release ID, checksum, or collection time.
Evidence: [first-match join](../../../core/release-report/release-report.service.ts#L357-L372), [available metadata](../../../core/release-report/ado-api/interfaces.ts#L467-L479).

## Failure behavior

| Failure | Observed outcome | Evidence |
| --- | --- | --- |
| Missing token, authentication, or release read failure | The report call fails. | [service](../../../core/release-report/release-report.service.ts#L47-L60), [client](../../../core/release-report/ado-api/client.ts#L123-L151). |
| Compliance read or normalization fails | The compliance section becomes `null`. | [handler](../../../core/release-report/release-report.service.ts#L172-L177). |
| Build detail or comparison fails | The build becomes `null` and is removed from the output. | [handler and filtering](../../../core/release-report/release-report.service.ts#L270-L286). |
| Coverage read fails or shape is unsupported | Coverage fields are omitted. | [handlers](../../../core/release-report/release-report.service.ts#L210-L252). |
| Attachment read or JSON parsing fails | That test report is removed from the joined evidence. | [attachment fallback](../../../core/release-report/ado-api/build.ts#L108-L110), [service filtering](../../../core/release-report/release-report.service.ts#L300-L320). |
| Related work item read fails | No local handler converts this error into a partial report. | [work item collection](../../../core/release-report/release-report.service.ts#L327-L354). |
| No qualifying production run exists | Production identity is empty and comparisons can contain only `changes: []`. | [baseline fallback](../../../core/release-report/ado-api/git.ts#L127-L131), [comparison fallback](../../../core/release-report/ado-api/git.ts#L322-L329), [returned object](../../../core/release-report/ado-api/git.ts#L385-L429). |

## Findings for reproduction

### Collector finding 1: Missing modules block exact reproduction

Evidence: [client imports](../../../core/release-report/ado-api/client.ts#L13-L17), [compliance imports](../../../core/release-report/ado-api/client.ts#L54-L60), [service imports](../../../core/release-report/release-report.service.ts#L10-L16).
`ado-api/coverage.ts`, `ado-api/release-compliance.ts`, service `interfaces`, and the Drizzle module are absent.
The supplied folder also has no package manifest, lockfile, or TypeScript configuration.
Consequence: Compilation and exact rule reproduction are unavailable from this copy.
Owner: Unknown.
Next action: Obtain missing rule sources or define reviewed replacement contracts.

### Collector finding 2: Failure states lose evidence

Evidence: [build filtering](../../../core/release-report/release-report.service.ts#L270-L289), [test report filtering](../../../core/release-report/release-report.service.ts#L305-L324).
Consequence: Consumers cannot distinguish absent evidence from excluded data using the returned report alone.
Owner: Unknown.
Next action: Record a section status, attempted identity, and error locator for each failed collection.

### Collector finding 3: Deployment and repository mappings require configuration

Evidence: [pipeline name matching](../../../core/release-report/ado-api/pipeline.ts#L15-L19), [build repository label](../../../core/release-report/ado-api/build.ts#L189-L202), [baseline rules](../../../core/release-report/ado-api/pipeline.ts#L80-L159).
Consequence: Pipeline naming changes or incomplete history can select the wrong repository or production baseline.
Owner: Unknown.
Next action: Bind repository and pipeline IDs explicitly and retain deployment selection evidence.

### Collector finding 4: Environment settings are embedded

Evidence: [client defaults](../../../core/release-report/ado-api/client.ts#L95-L120), [TLS settings](../../../core/release-report/ado-api/client.ts#L129-L141), [contribution page context](../../../core/release-report/ado-api/extension/PipelineRuns.ts#L30-L39).
The API client and contribution request disable TLS certificate verification.
The cloud base URL is fixed and several request fields embed one organization's context.
Consequence: Direct reuse carries machine assumptions and weakens transport verification.
Owner: Unknown.
Next action: Use Workbench root configuration and verified TLS defaults.

### Collector finding 5: Test attachment statistics have no selected-run reconciliation

Evidence: [first-match join](../../../core/release-report/release-report.service.ts#L357-L372), [attachment metadata](../../../core/release-report/ado-api/interfaces.ts#L467-L479).
Consequence: Duplicate requirements can show statistics from an arbitrary build order.
Owner: Unknown.
Next action: Preserve build-specific statistics and define an explicit selection or aggregation policy.

## Read and write boundary

The inspected report service reads remote data and returns an in-memory report.
Its database persistence call is commented out.
No inspected report call uploads or attaches the generated report to ADO.
Evidence: [return and disabled persistence](../../../core/release-report/release-report.service.ts#L84-L101).

The shared ADO client also exposes unrelated write operations.
These include work item relations, test cases, test runs, test plans, and PR comments.
The report service does not invoke those write operations.
Evidence: [client bindings](../../../core/release-report/ado-api/client.ts#L194-L248), [relation mutation](../../../core/release-report/ado-api/workitem.ts#L113-L143).

## Dependencies and evidence limits

Observed collector imports include NestJS, Azure DevOps SDK, Zod, Day.js, and `typed-rest-client`.
Internal package names include `ratan-ado-api`, `ratan-sonarqube-api`, and `ratan-markdown-tool`.
The separate Sonar wrapper imports `sonarqube-webapis` and Axios types.
Its server URL is embedded in source.
Evidence: [service imports](../../../core/release-report/release-report.service.ts#L1-L16), [build imports](../../../core/release-report/ado-api/build.ts#L1-L9), [HTTP wrapper](../../../core/release-report/ado-api/extension/HierarchyQuery.ts#L1-L2), [Sonar wrapper](../../../core/release-report/sonarqube-api/client.ts#L5-L35).

Dependency versions and original package identities are unavailable.
No build, runtime execution, endpoint call, or credential check occurred.
No result proves deployment state, compliance policy, or passing business behavior.

## Review status

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - This analysis uses static source inspection only.
```
