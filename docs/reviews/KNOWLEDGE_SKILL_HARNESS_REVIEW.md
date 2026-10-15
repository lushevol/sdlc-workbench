# Knowledge skill and harness review

Date: 16 October 2026.
Scope: Complete the interrupted ingestion, governance, and verification skill update.
Consumer: Agents that create evidence-linked knowledge from historical materials and implementation sources.
Risk: Moderate. Installed package contents and final audit checks affect generated workspace use.

## Supported changes

The [ingestion skill](../../skills/ingest-knowledge/SKILL.md) now defines ordered checkpoints with inputs, outputs, and completion conditions.
Its [workflow](../../skills/ingest-knowledge/references/workflow.md) explains preparation, immutable events, repair, and final checks.
Its [evidence guide](../../skills/ingest-knowledge/references/evidence.md) supplies claim, feature, assertion, and retrieval worksheets.
The [plan template](../../skills/ingest-knowledge/assets/check-plan.yaml) selects documents, repository locations, and compatible execution results.

The [governance skill](../../skills/govern-knowledge/SKILL.md) orders final formatting before event creation.
The [verification skill](../../skills/verify-implementation/SKILL.md) separates assertion inspection, matching execution, and broader unverified behavior.
The [installed harness](../../core/ingestion/harness.py) checks retention, local citations, captured code, execution hashes, and prepared content.
Runtime source remains under `core/`; generated workspaces receive guides and shared skills.

## Evidence and corrections

The [authentication investigation](AUTHENTICATION_SESSION_PILOT_REPORT.md) records the earlier evidence failures that motivated this update.
Those failures included incomplete citations, stale execution hashes, and document changes after event creation.
The present review also exercised fresh ingestion and preserved existing project evidence.

| Finding and evidence | Consequence | Owner | Completed action |
| --- | --- | --- | --- |
| Timing and assertion citations omitted relevant code in the authentication investigation. | Resolving links could support incorrect explanations. | unknown | Added claim and assertion worksheets with exact-source review. |
| An earlier pilot result used a different source hash. | A passing result could describe earlier implementation bytes. | unknown | Added retained result comparisons against pinned Git blobs. |
| Formatting changed after an immutable event was created. | The event no longer bound final document bytes. | unknown | Added preparation and final content comparisons. |
| The first isolated ingestion failed with `manifest_prefix_changed`. | Initialized workspaces could not add their first source records. | unknown | Allowed first additions to an empty manifest; retained existing record checks. |
| Review reproduced candidate deletion and uppercase Markdown audit bypasses. | Retained knowledge or required events could disappear from checks. | unknown | Added missing-document checks and consistent Markdown extension handling. |
| Review reproduced a correction branch from an existing event. | New correction checks could miss an existing successor. | unknown | Checked correction relationships across historical and new events. |
| macOS temporary directory aliases failed output checks. | Valid temporary report destinations were rejected. | unknown | Resolved parent aliases and retained exclusive output creation. |
| The independent trial found ambiguous finding placement. | Agents could save finding records in the wrong directory. | unknown | Named `knowledge/findings/` explicitly. |
| The reader treated unspecified retries as zero retries. | A missing rule could become invented policy. | unknown | Corrected the reading and added an explicit evidence example. |

The harness regressions reproduce the mechanical defects and their corrected outcomes.
They cover consequential boundaries rather than generated wording.

## Actual validation

| Check | Result | Limit |
| --- | --- | --- |
| Harness regression suite | `PASSED`: 23 tests. | Local fixtures; no business execution. |
| Affected runtime and interface suite | `PASSED`: 156 tests. | Excludes graph tests; includes catalogs, governance, providers, CLI, and workspace initialization. |
| Complete runtime suite | `FAILED`: 305 passed; one graph viewer failure. | The failure belongs to pre-existing concurrent graph work. |
| Existing project harness | `PASSED`: 13 documents, 404 links, 250 line ranges, 89 code captures, five execution source hashes. | Checks selected evidence; it does not prove semantic support. |
| Existing evidence retention | `PASSED`: 323 raw files, 322 manifest records, 25 audit files. | No knowledge or governance record changed during this stage. |
| Independent ingestion trial | `PASSED`: four governed records, four new events, 20 links, 11 line ranges. | Two fictional historical sources in a temporary workspace. |
| Independent retrieval | Three questions completed; one semantic overstatement corrected. | The evaluating model was not recorded. |
| Review-mode trial | `PASSED`; originals, source catalog, raw manifest, and audit bytes remained unchanged. | External plain-text citations received manual review. |
| Three skill structure checks | `PASSED`. | Naming, frontmatter, and scaffold checks only. |
| Changed guide and report links | `PASSED`: 35 local destinations. | Ten external destinations or heading fragments remain unchecked. |
| Limited writing checks | `PASSED`: prose line length, whitespace, and final newlines. | These checks do not complete an ASD review. |
| Standard isolated wheel build | `FAILED`: build dependency retrieval unavailable. | The sandbox blocked the configured package proxy. |
| Wheel build with installed build tools | `PASSED`. | Used `--no-build-isolation` without dependency downloads. |
| Fresh wheel installation and workspace | `PASSED`: initialization, validation, imports, resources, and all three harness checkpoints. | Offline dependency copies; macOS only. |

The complete-suite failure is `GraphViewerRendererTests.test_repository_inventory_full_labels_semantic_routes_and_api_trace`.
Its graph fixture omits expected injection and type edges.
Owner: unknown; the concurrent graph stage owns the affected files.
Consequence: the complete runtime suite remains unsuccessful.
Next action: resolve the fixture or extractor behavior within that stage, then rerun its checks.

The independent trial preserved its original failed preparation result.
After the fix, it passed against the same original baseline.
The reader located historical context, conflicting timeouts, missing owners, and unresolved retry policy through the index.
No source document supplied implementation, deployment, execution, or approval evidence.

The fresh installation supplies eight knowledge schemas, six templates, seven core guides, and all four ingestion skill assets.
Its generated workspace contains no core Python source, runtime tests, package configuration, or live knowledge.
Package imports resolve to the isolated installation.

## Commands and evidence limits

Run these commands from the standalone source checkout:

```sh
.venv/bin/python -m unittest tests.test_ingestion_harness -v
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip wheel . --no-deps --wheel-dir dist
.venv/bin/python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
ai-sdlc --workspace PATH validate
```

The [workflow](../../skills/ingest-knowledge/references/workflow.md#harness-commands) defines the checkpoint commands and supported plan fields.
Local execution records remain in ignored `.workbench/ingestion/skill-review-resumed-20261016/` and temporary validation directories.
The temporary fictional records are evaluation inputs and are excluded from this repository.

Clearer instructions can reduce decisions that a model must infer.
This is an inference; this stage did not evaluate a named weaker model.
The checker cannot determine source truth, citation meaning, assertion coverage, approval, or complete ASD writing correctness.
Windows execution remains untested.
Business behavior verification and publication remain outside this stage.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - A capable-agent trial does not establish reliability for less capable models.
```
