# Native ADO bridge and consumer constraints

> **Critical conclusion:** Retain the native ADO integration for existing report consumers. The requested skills do not supply its executable contracts. No user action is required for this assessment; any replacement is a separate implementation scope.

Assessed on 13 November 2026 (Asia/Singapore) for the [user request](user-input.md#exact-user-input). Local HEAD: `79a4104035785b7d8c37e6d424d5d4c888104eee`. `git status --short` returned no changes for the inspected native bridge, provider, report collector, and connector registry paths. This is source and assertion inspection; no live ADO execution or replacement was performed.

## Result

Azure DevOps skills cannot replace the existing native ADO integration directly. The skills are agent instructions that depend on a separately configured Azure DevOps MCP server. Workbench has executable protocols, exact grants, raw readers, and a report collector that calls those readers by exact name. Even if another server can reach equivalent REST endpoints, a compatibility implementation and conformance verification are still required.

The upstream repository identifies seven example skills and explicitly requires the Azure DevOps MCP server: [README at b418a6c8, lines 23–53](https://github.com/microsoft/azure-devops-skills/blob/b418a6c8fa9fd622274882a1378e664df746f356/README.md#L23-L53). This does not itself implement Workbench's reader, response, grant, or evidence contracts.

## Current callable grant surface

[registry/tools.yaml:69](../../../registry/tools.yaml#L69) enables `list` and `call` for `external-ado`. It grants **26 exact tool names**: 12 imported reads and all 14 ADO `report_*` readers. Listing more tools does not grant them.

The 12 imported granted reads are `wit_list_projects`, `wit_get_work_item`, `wit_get_work_items_batch_by_ids`, `wit_list_work_item_comments`, `wit_get_query_results_by_id`, `repo_list_repos_by_project`, `repo_get_file_content`, `repo_list_directory`, `repo_get_pull_request_by_id`, `repo_get_pull_request_changes`, `search_code`, and `search_workitem`.

[server.js:71](../../../core/connectors/workbench/server.js#L71) registers imported `configureAdoTools` and then `configureReportReadTools`. The 14 report readers therefore extend the imported ADO package; package-only comparison would omit a current consumer.

## Fourteen ADO report readers

Definitions are at [release-readers.js:39](../../../core/connectors/workbench/release-readers.js#L39). Unless stated otherwise, endpoints use API version `7.1`; inputs reject unknown fields. String inputs are nonempty and at most 8,192 characters; numerical identities are positive integers.

| Exact tool | Input and endpoint semantics that a replacement must preserve |
| --- | --- |
| `report_work_items` | 1–200 IDs, optional project and historical `asOf`; POST `wit/workitemsbatch` with `$expand: All`. Complete raw work items and relations. |
| `report_builds` | Project and 1–200 IDs; `buildIds` and `$top=IDs.length`; original raw fields. |
| `report_build_timeline` | Project/build ID; complete build timeline. |
| `report_build_artifacts` | Project/build ID; original artifact metadata and links. |
| `report_build_logs` | Project/build ID; log metadata, without downloading every log. |
| `report_build_properties` | Project/build ID; raw properties including analysis identities. |
| `report_attachment` | Project/build/timeline/record/type/name; exact timeline attachment bytes. |
| `report_coverage` | Project/build ID; `test/codecoverage` with `flags=7`. |
| `report_deployments` | Project/pipeline ID, optional keyword and continuation token; POST Contribution `HierarchyQuery` with API version `5.0-preview.1` and `ms.vss-build-web.runs-data-provider`. Pipeline run stage evidence, rather than a generic list of builds. |
| `report_branches` | Project/repository, optional branch filter and continuation token; branch refs with `$top=1000`; filter normalized to `heads/`. |
| `report_compare` | Project/repository and exact base/target **commit** identities; optional common-commit mode, skip and top; `diffs/commits`. Skip defaults to 0, top to 100 (maximum 1000). |
| `report_commits` | Project/repository and exact base/target **commit** versions; includes linked work items; explicit skip/top with defaults 0/100 and maximum top 1000. |
| `report_commit_changes` | Project/repository/exact commit; changed-file metadata with explicit skip/top, defaults 0/100 and maximum top 1000. |
| `report_file` | Project/repository/path/exact **commit** identity; `items` with `includeContent=true` and commit version descriptor. |

## Executable contracts beyond endpoint coverage

| Contract | Inspected implementation and implication |
| --- | --- |
| Native provider process | [connectors.py:52](../../../core/providers/connectors.py#L52) sends one JSON request to an explicit command argument array, appending `--workspace`; uses no shell. Requires `status=SUCCEEDED`, tool discovery schemas, and MCP result objects. A Markdown skill is not this process. |
| Exact grants | [connectors.py:41](../../../core/providers/connectors.py#L41) validates unique names; line 54 denies absent tools **before process startup**. Native discovery annotates every tool with `allowed`. No wildcard or empty-list grant exists. |
| Selected workspace configuration | [config.js:5](../../../core/connectors/workbench/config.js#L5) requires an absolute workspace, loads its root `.env`, and lets process values override it. Resolves relative CA and review-guide paths against that workspace; ADO variables are `AZURE_DEVOPS_ORG_URL` and `AZURE_DEVOPS_PAT`. Do not assume upstream authentication/configuration is interchangeable. |
| Validation and sanitized failures | [release-readers.js:148](../../../core/connectors/workbench/release-readers.js#L148) validates exact reader/connector and strict inputs. [bridge.js:28](../../../core/connectors/workbench/bridge.js#L28) validates request shape, returns fixed connector failure messages, and keeps stdout a single JSON envelope. |
| Inline/native result | [release-readers.js:348](../../../core/connectors/workbench/release-readers.js#L348) returns both `structuredContent: {data, headers, http_status}` and text JSON. Inline raw response limit is 4 MiB; complete serialized MCP payload is limited to 4 MiB minus 4,096 bytes. The Python provider separately limits process output to 4 MiB. |
| Raw collection/session result | [release-session.js:10](../../../core/connectors/workbench/release-session.js#L10) implements line-delimited `init`/`call`/`list`/`close` with IDs and exact tool grants. Calls require an evidence path, confined below the selected run directory; existing paths and duplicate claimed destinations are rejected. [release-readers.js:290](../../../core/connectors/workbench/release-readers.js#L290) streams exact bytes to exclusive files, computes SHA-256 and byte size, and returns metadata rather than large content. Non-2xx bodies are retained with `HTTP_<status>` errors. The streaming branch has no fixed 4 MiB body cap; deadlines and disk remain limiting. |
| Pagination/header preservation | [release-readers.js:310](../../../core/connectors/workbench/release-readers.js#L310) preserves both continuation header spellings, `Retry-After`, content type, ETag, and last-modified. Collector [release_report.py:273](../../../core/release_report.py#L273) handles explicit pages, repeated-page and incomplete-page errors, deadlines, and entity limits; deployments and branches use separate continuation logic. Summary text would lose these contracts. |
| Network/session behavior | [release-readers.js:191](../../../core/connectors/workbench/release-readers.js#L191) uses a persistent keep-alive client, PAT Basic authentication, configured proxy and CA with TLS validation, no redirects, request and collection deadlines, bounded concurrency, cancellation, and metrics. At most four attempts for selected transient HTTP/network errors; `Retry-After` pacing and throttle-driven concurrency reduction apply. These behaviors are executable rather than agent advice. |
| Report consumer coupling | [release_report.py:146](../../../core/release_report.py#L146) requires matching `connector.mcp` resources. Lines 182–249 instantiate `ConnectorSession`, enforce `call` plus exact reader grants, deduplicate identical calls, retain raw evidence, and journal/checkpoint each request. Build enrichment calls all timeline/artifact/log/property/coverage readers; attachments and exact source comparisons feed the report. Changing only skill files leaves these callers unresolved. |

## Verification evidence inspected

Inspected assertions, not rerun results:

- [release-session.test.js:62](../../../core/connectors/workbench/release-session.test.js#L62): bounded actual mock HTTP concurrency and one client; exact grants and argument validation send zero requests; Retry-After pacing; large streamed bytes; transient retry; retained forbidden body; confined paths; deadlines; source comparison semantics; serialized inline limits; configured TLS/proxy behavior.
- [test_release_report_integration.py:263](../../../tests/test_release_report_integration.py#L263): a 5 MiB attachment must retain exact bytes, SHA-256, both expected fixture records, a small manifest, and exactly two attachment requests. Lines 280–287 assert an ungranted coverage read makes zero HTTP requests and yields partial collection with `TOOL_NOT_GRANTED`.
- [docs/RELEASE_REPORT.md:24](../../../docs/RELEASE_REPORT.md#L24) documents the native source checkout, root variables, exact source grants, manifest, journal, checkpoint, and hash-bound evidence consumer contract.

## Replacement condition

Retain the native ADO provider/readers for current consumers. Upstream skills can be optional workflow guidance. Replacing native execution requires a separately scoped adapter that preserves exact supported calls and raw evidence semantics, followed by contract tests and authorized live ADO verification. Equivalent tool names or endpoint availability alone do not establish equivalence.
