---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Verification uses mock ADO and SonarQube services. Company endpoints and native Windows remain untested.
---

# Generate a release report

Collect release information with an ADO **Release work item ID**.
Render the saved snapshot into local HTML.
Collection and rendering use separate interfaces.
Release Clinic supplies separate compliance documents through direct links.

## Prepare the workspace

Install Workbench and the optional Node connectors through the [setup guide](SETUP.md).
Collection uses existing root variables from the [connector guide](CONNECTORS.md#maintain-variables-at-the-workspace-root).
Set `AZURE_DEVOPS_ORG_URL` and `AZURE_DEVOPS_PAT` for ADO reads.
Set `SONAR_BASE_URL` and `SONAR_TOKEN` when builds publish a Sonar project identity.
Keep credentials in the selected workspace's ignored `.env` file.

The source checkout registers `release-report`, `external-ado`, and `external-sonar`.
Generated workspaces start with empty tool catalogs.
Merge the [report example](../registry/examples/release-report.yaml) and the selected [connector examples](../registry/examples/connectors.yaml).
Preserve existing catalog entries.
Set connector commands to the source checkout's absolute `core/connectors/workbench/bridge.js` path.
The installed wheel contains Python reporting modules. It requires that separate connector checkout for collection.

Discover connector schemas and exact grants before collecting data.

```sh
ai-sdlc --workspace PATH status
ai-sdlc --workspace PATH call external-ado list
ai-sdlc --workspace PATH call external-sonar list
```

Grant `collect` on the report resource.
Each source also requires `call` and the exact requested tool names in `config.allowed_tools`.
The [connector example](../registry/examples/connectors.yaml) includes the report readers.
Missing grants produce explicit collection errors.

## Collect, verify, and render

Replace `501` with the Release work item ID.
Select a new output directory inside the selected workspace.

```sh
ai-sdlc --workspace PATH release-report collect 501 --output-dir reports/release-501
ai-sdlc --workspace PATH release-report verify reports/release-501/manifest.json
ai-sdlc --workspace PATH release-report render reports/release-501/manifest.json --output reports/release-501.html
```

Collection returns `manifest_path`, `action_id`, `collection_status`, source identities, and request metrics.
The retained action contains a `release-report/` directory under `.workbench/runs/ACTION_ID/`.
Without `--output-dir`, use the returned manifest path directly.
The export contains the snapshot, manifest, request journal, checkpoint, and hashed evidence files.
Move the complete export when sharing retained data.
Local Clinic links still require their separately managed files.

Rendering makes no service requests and needs no service credentials.
Verification checks the snapshot identity and all declared evidence hashes.
It does not establish data completeness or business correctness.
HTML includes bounded previews and links to the complete snapshot and retained evidence.

Use `--resume MANIFEST` to compare a prior collection with a fresh collection.
The collector retains the prior manifest identity and rechecks the release revision.
It collects source data again instead of reusing old mutable responses.
A revision mismatch produces a partial report and preserves both collections.

## Report contents and limits

The report preserves all returned release fields and expanded relations.
It derives builds from `Custom.LatestPipelineRuns` and ADO Build artifact links.
It collects related work items, tests, defects, build metadata, timelines, artifacts, logs, properties, and ADO coverage.
It retains test evidence from `generatetestreport` task attachments named `rtm.json`.
It compares candidate commits with branch tips, `main`, and the selected production baseline.
It retains commit, file, work item, and test relationships.
Binary artifacts and log contents remain metadata links unless the report explicitly reads them.

Production selection follows the supplied source's `prod` and `rollback_prod` stage rules.
That selection is source behavior. It does not establish deployment authorization.
Unknown baselines, absent branches, failed pages, and missing builds remain explicit.

Sonar enrichment requires a project identity in build properties.
Supported keys include `sonar.projectKey`, `SonarQube.ProjectKey`, and `sonarProjectKey`.
Branch and pull request selectors remain distinct.
Measures, gate results, issues, hotspots, and analysis history remain separate from ADO coverage.
Current measures have verified association only when the current analysis matches the build revision.
Other current data carries `association_status: current_snapshot`.
An absent project identity appears as unavailable.

Compliance links use matching Release Clinic HTML attachments or local reports.
Local reports use `TDA_OUTPUT_DIR` or `.workbench/release-clinic/reports/`.
Their supported filename prefixes are `TDAReport_`, `TDA_Report_`, `Annotated_TDA_Report_`, and `Annotated_TDAReport_`.
Local filenames must end with the release ID, optionally followed by a numbered duplicate suffix.
The report collector does not fetch or parse Clinic HTML.
The renderer does not overwrite Clinic reports.

`collection_status` describes the collected data:

| State | Meaning |
| --- | --- |
| `complete` | Required reads completed without recorded collection errors. Explicit optional unavailability can remain. |
| `partial` | Release data exists, but errors or revision conflicts limit the collection. |
| `failed` | The requested release could not be collected. |

A partial report remains inspectable. Check `collection_status` even when the collection command succeeds.
Collection status does not establish production readiness, test success, or release approval.

## Performance and configuration

One collection starts at most one process for each required connector.
Each process reuses one HTTP client and connection pools.
The report readers reuse existing configuration, authentication settings, proxy handling, and declared Axios dependency.
They use raw REST requests so the scheduler can govern each HTTP attempt.
They do not change existing SDK-based connector operations.

The collector batches up to 200 unique work item IDs.
It coalesces identical requests within the collection and follows pagination.
Large responses stream into evidence files instead of connector JSON frames.
Retry delays apply to the source session, including successful responses with `Retry-After`.
Failed transient reads have bounded retries.
Source sessions close after completion or cancellation.

| Resource setting | Default | Supported values |
| --- | --- | --- |
| `ado_resource` | `external-ado` | Registered native ADO resource ID. |
| `sonar_resource` | `external-sonar` | Registered native Sonar resource ID. |
| `collection_timeout_seconds` | Workspace timeout | Number from 0.05 through 3600. The source example uses 300. |
| `request_timeout_seconds` | 30 | Number from 0.01 through 3600, within the remaining collection budget. |
| `ado_concurrency` | 6 | Integer from 1 through 32. |
| `sonar_concurrency` | 2 | Integer from 1 through 32. |
| `max_entities` | 20000 | Integer from 1 through 1000000. |

Metrics record attempts, retry counts, transferred bytes, concurrency, session counts, cache hits, and elapsed time.
Mock timing establishes scheduler behavior only.
Measure company endpoints before choosing production tuning values.

## Python and MCP interfaces

The Python interfaces use the installed package name.

```python
from ai_sdlc_workbench.release_report import collect_release_report
from ai_sdlc_workbench.release_report_contract import read_release_report
from ai_sdlc_workbench.release_report_render import render_release_report

result = collect_release_report(501, workspace="/path/to/workspace")
snapshot = read_release_report(result["manifest_path"])
render_release_report(result["manifest_path"], "/path/to/release-501.html")
```

MCP collection uses the same registered provider and evidence contract.
Call `workbench_call` with `resource_id: release-report`, `operation: collect`, and `arguments: {release_id: 501}`.
Use `workbench_status` for discovery and `workbench_runs` with `run_id` for retained action details.
See the [MCP guide](../adapters/mcp/README.md) for client setup.
