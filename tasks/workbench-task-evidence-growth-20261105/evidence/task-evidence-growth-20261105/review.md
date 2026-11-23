# Task evidence growth review

> **Critical conclusion: Reduce duplicate payloads and unnecessary evidence files through separate actions.**
>
> The 24 November scan found 20.513 GB across 59,949 regular evidence files.
> Duplicate bytes account for 12.732 GB. These totals do not establish safe deletion.
> Owner: Workbench maintainers. Next action: apply the [prioritized plan](#prioritized-optimization-plan) within an authorized implementation or cleanup scope.
> Evidence: [current assessment](#current-assessment-24-november-2026) and [capture configuration](../../../../e2e/audit.config.ts).

The [original user input](user-input.md#exact-user-input) defines the 5 November maintenance scope.
That stage changed capture behavior and shared procedures. The 24 November stage provides an assessment only.

## Follow-up request: 24 November 2026

Source: current Codex chat, 24 November 2026, Asia/Singapore.

> I found there are too many evidences files of different type in task, which most of them are useless, please check how to optimize it

Authorized scope: inspect current task evidence and propose concrete retention improvements.
Reuse this owning report. Preserve unrelated worktree changes.
Outcome: current evidence measured; producers and consumers inspected; optimization plan prepared.
Deletion candidates require consumer review under the [cleanup procedure](../../../README.md#evidence-priorities-and-cleanup).

## Current assessment: 24 November 2026

Inspected Workbench revision: `e72f75c5527a98074b26e5e3f6aa36abe705a7fb`.
Unrelated CES and domain-extractor work continued during inspection. All such changes remained outside this assessment.
Scope: regular files below task `evidence/` directories, excluding symlinks and external checkout targets.
The scan used `os.walk(..., followlinks=False)`, `lstat()`, and regular-file checks.
Sizes are decimal GB and logical bytes. They do not predict allocated disk recovery.
The figures capture one local observation before this report update, without a locked filesystem snapshot.

| Observation | Measured value | Implication |
| --- | ---: | --- |
| Regular evidence files | 59,949; 20,512,657,403 bytes | Both navigation and storage need attention. |
| Symlink entries | 48,837 | Following aliases overcounts payloads; aliases still increase visible clutter. |
| Tracked regular evidence | 52,514; approximately 1.698 GB | Repository clutter differs from local disk use. |
| Ignored regular evidence | 7,433; approximately 18.815 GB | Existing ignore rules do not reclaim local bytes. |
| UI coverage task | 49,635; approximately 20.222 GB | This task holds 98.6% of measured bytes. |
| Files below 1 KiB | 15,157; approximately 10.9 MB | Numerous small files create navigation work despite limited disk cost. |
| Empty files | 39 | Some command receipts can replace empty logs. |
| Duplicate payload groups | 3,184 groups; 12,504 extra copies | Hash equality identifies repeated bytes, without establishing redundant provenance. |
| Redundant logical bytes | 12,731,563,852; 62.1% of total | This is a theoretical consolidation estimate, before consumer and protection review. |

The duplicate scan grouped regular files by size, then hashed complete contents with SHA-256.
It excluded symlink aliases. It retained aggregate findings instead of another complete file inventory.

| File type | Regular files | Logical bytes |
| --- | ---: | ---: |
| ZIP | 4,806 | 18,610,017,012 |
| JSON | 34,242 | 724,541,571 |
| PNG | 7,776 | 755,301,149 |
| HTML | 3,984 | 204,546,382 |
| JavaScript | 658 | 95,222,446 |
| TypeScript | 3,860 | 28,284,975 |

File type alone cannot determine usefulness. Raw observations, assertions, and provenance can require any of these formats.
The findings establish substantial duplication. They do not establish that most retained evidence lacks value.

### Confirmed storage and navigation causes

Historical traces account for 12,404,483,500 redundant bytes across 3,202 extra ZIP copies.
The [existing example inventory](measurements.json) identifies the run-007 trace in three locations.
The locations are Playwright artifacts, case attachments, and HTML report data.
All three still contain 24,317,406 identical bytes.
Verified SHA-256: `aba8ff0c5064b604acc19e625afbcef02d3bffcf6b9bdfb28c804296039011b0`.
Current results and manifests can reference separate copies. Cleanup requires consumer and provenance review.

The [current settings](../../../../e2e/support/audit-settings.ts) already default to failure traces and omit HTML exports.
The [current reporter](../../../../e2e/audit.reporter.ts) also reuses attachments within durable run output.
These improvements address future trace copying. The historical copies remain present.

| Current source or example | Observed issue | Proposed correction and limit |
| --- | --- | --- |
| [Screenshot capture](../../../../e2e/support/audit-fixture.ts) | Each frame gets a JSON sidecar. Consolidated `frames.json` contains the same frame metadata. | Stop new sidecars after a focused compatibility check. Keep frame metadata, required screenshots, and historical manifest bytes. |
| [Audit summary reader](../../../../e2e/scripts/summarize-audit.py) | The reader consumes `frames.json` and excludes numbered sidecars from supplemental observations. | Use this existing consolidated metadata. No inspected direct reader required numbered sidecars. External consumers remain unverified. |
| [Source capture](../../../../e2e/audit.reporter.ts) | Every run copies matching files from the entire E2E tree and package manifests. | Reuse verified exact revisions or retained source variants. Preserve required unavailable, changed, and uncommitted bytes. |
| [Source validator](../../../../e2e/scripts/validate-audit-report.py) | Existing readers support source variants and run snapshots. | Reuse these contracts before designing another storage format. Resolve exact dependency scope before narrowing capture. |
| [Audit output defaults](../../../../e2e/audit.config.ts) | Routine harness runs default into the historical UI coverage task. | Use explicit owning-task output for retained investigations. Keep disposable harness output local and ignored. Preserve immediate durable case checkpoints. |
| [Screenshot settings](../../../../e2e/audit.config.ts) and [fixture teardown](../../../../e2e/support/audit-fixture.ts) | Automatic screenshots coexist with custom final and canonical-step captures. | Review overlapping final captures. Preserve required step observations, timestamps, assertions, and failure evidence. |
| [Case and run records](../../../../e2e/audit.reporter.ts) | Started, result, frame, artifact, progress, native report, and run records overlap. | Preserve consumer and interruption contracts. Consolidate only after tracing each reader; some separate records remain necessary. |
| [Routine maintenance evidence](../../../workbench-dependency-download-timeouts-20261103/evidence/dependency-download-timeouts-20261103/) | Separate check JSON files and logs increase file count around one maintenance outcome. | Put routine check receipts in the living record. Retain separate outputs only for an actual consumer or claim. |

The historical `report-002` through `report-006` directories contain approximately 63–65 MB `case-results.json` files each.
These are complete report snapshots. Their overlap requires semantic comparison before selecting retained baselines.
Equal file sizes do not establish equal contents.

### Prioritized optimization plan

1. **Simplify new task evidence immediately.** Use one living record for requests, decisions, findings, and routine check receipts.
   Keep separate payloads for necessary assertions, failures, contradictions, unresolved questions, reproduction, recovery, or protected provenance.
   This applies the [existing policy](../../../README.md#critical-evidence-and-reusable-payloads), without another mandatory report or index.
2. **Review historical trace and HTML copies first.** Start with the UI coverage task and byte-identical trace groups.
   Select canonical retained payloads, inspect all consumers, and record exact recovery information under the cleanup procedure.
   Preserve frozen manifests, registered snapshots, and immutable audits. Leave protected copies when consolidation cannot preserve their contracts.
3. **Stop low-value producer duplication.** Remove new screenshot sidecars before changing broader result formats.
   Reuse recoverable source identities or existing source variants. Route each retained run to its actual owning task.
   Run focused reader, hash, screenshot, and interruption checks before changing capture defaults.
4. **Keep generated views optional.** Generate HTML and galleries for a current reviewer, using local ignored storage for derivative copies.
   Keep one current human-facing report. Preserve separately required decision baselines and their exact versions.
5. **Review file growth at existing checkpoints.** Record file count, retained bytes, and material increases in the living record.
   Choose evidence from its purpose and consumer. Avoid blanket extension deletion, expiry, or another budget subsystem.

For a small maintenance task, the target is one current record plus necessary payloads.
Record command, source identity, environment, exit status, assertion outcomes, counts, and limits in a compact check table.
Do not create separate `document-checks.json`, `verification-summary.json`, or empty logs solely to prove a routine successful command ran.
Retain such files when a real consumer, machine assertion, failure investigation, or protected evidence contract needs them.
Large executions retain their existing case results, one run binding, and indexed canonical payloads.
This target preserves immediate case saving and exact observations while reducing incidental file creation.

### Assessment checks and scope limits

| Performed check | Result and limit |
| --- | --- |
| Regular-file inventory and symlink exclusion | Completed; the independent inventories agreed on counts and extension bytes. |
| Whole-content SHA-256 duplicate scan | Completed; aggregates and the trace example above were verified. This does not authorize deletion. |
| Active producer and reader inspection | Completed for audit configuration, reporter, fixture, summary reader, source validator, and retention tests. |
| Retention procedure review | Existing [retention](../../../README.md#critical-evidence-and-reusable-payloads), [growth](../../../README.md#control-evidence-growth-before-execution), and [cleanup](../../../README.md#evidence-priorities-and-cleanup) rules already support these recommendations. |
| Capability lookup | The installed CLI returned an unrelated ADO declaration. No applicable capability or new reusable contract was introduced. |
| Documentation checks | `git diff --check` passed. All 26 local Markdown links and requested heading anchors resolved. |
| Independent assessment review | Completed; duplicate counts and historical wording were corrected. No actionable issue remained. |
| Runtime and business execution | Not run; this stage changes the assessment only. Producer changes and historical cleanup remain proposals. |

Current documentation requires no new runtime claims. This assessment extends the existing report instead of adding evidence files.
No historical evidence was deleted, relocated, or rewritten. No complete cleanup consumer audit was performed.
Check outcomes above describe automated inspection. ASD writing review remains pending.

## Historical measurements: 5 November 2026

Source baseline: `9effd24be5ac76ee9ffddc7472cac99d2603dc1e`.
The scan covered regular files under `tasks/`, `docs/evidence/`, and `evidence/`.
It excluded symlinks, independent repositories, `.git`, and `.workbench`.
Values use decimal GB and logical file sizes. They do not measure allocated disk savings.
This is one local observation, without a historical growth series.

| Observation | Measured value | Consequence |
| --- | --- | --- |
| All scanned evidence | 58,011 files; 20.509 GB | Evidence has substantial local storage cost. |
| UI test coverage task | 20.223 GB | One task accounts for 98.8% of task bytes. |
| ZIP files | 18.610 GB | Trace capture dominates volume. |
| Ignored evidence | 18.830 GB | Git exclusion alone does not control local growth. |
| Tracked evidence | 1.679 GB | Reports and retained artifacts also increase repository size. |
| Exact duplicate bytes | 12.731 GB | Repeated payloads explain 62.1% of measured bytes. |
| Markdown files | 0.027 GB | Report text is a smaller disk contributor. |

The [measurement record](measurements.json) retains methods, exclusions, totals, and four hashed examples.
Identical hashes establish repeated bytes. They do not establish safe deletion or equivalent provenance.

## Confirmed causes

### Trace capture and copying

The original audit configuration enabled traces for every test.
The original audit reporter copied attachments from durable run storage into each case.
The HTML reporter created another payload copy.

The scan found 1,601 trace ZIPs in each of three output categories.
Each category contained exactly 6.202 GB: Playwright artifacts, case attachments, and HTML report data.
One canonical trace could avoid approximately 12.404 GB of this observed duplication.
This estimate describes logical bytes. Existing consumers and registered snapshots still require review before cleanup.

### Repeated complete reports

Successive `report-002` through `report-006` bundles contain large `case-results.json` files.
Each file measures approximately 62.7–65.0 MB.
They repeat complete result collections across reporting rounds.
Use one living report during active work. Preserve exact versions when decisions require frozen baselines.

### Conflicting capture instructions

The task guide already prohibited redundant reports and unchanged checkpoints.
Other instructions required copies from every external output location and new traceability artifacts for saved phases.
Those instructions encouraged duplication despite the general retention rule.
The revised [growth controls](../../../README.md#control-evidence-growth-before-execution) establish one canonical payload and shared run bindings.

## Prevention changes

The E2E reporter reuses attachments already retained inside the unique run directory.
It copies external payloads into durable case storage.
Case manifests include referenced payloads, with their hashes and sizes.
Required screenshots and immediate case checkpoints remain available.

Routine local audit runs retain traces for failed cases.
Set `E2E_AUDIT_TRACE=on` before runs that require successful timing, request, or lifecycle traces.
A missing passing trace requires another authorized execution when its claim needs that evidence.
Configured application runs retain their existing trace restrictions.

HTML report bundles require `E2E_AUDIT_HTML=1`.
This export can duplicate payloads. Enable it when a current reviewer needs the bundle.
The audit reporter remains active with either setting.

Shared procedures now reuse canonical payloads and bind shared metadata once per run.
Each case retains its own outcomes and references the run binding.
The evidence index links the progress inventory and changes when its claims or navigation change.
Frozen snapshots, contradictory results, consequential failures, and immutable audits retain their protection.

These changes reduce future capture volume. They do not implement a general evidence budget or automatic expiry.
The core action store still retains dispatched action records.
No new dependency, storage service, or source migration is required.

## Existing evidence disposition

Existing evidence remains unchanged.
A future cleanup must identify each consumer, canonical retained path, source identity, and hash before removing a copy.
Retain registered snapshots and immutable audit bytes under their existing contracts.
Record authorized removals in one manifest. Repair active links and verify retained hashes.

The ignored `.workbench` directory also contains several browser installations and local runtime copies.
A separate local scan measured 5.592 GB across 163,037 regular files there.
Those bytes are outside the evidence totals above.
Runtime lifecycle cleanup requires its own inventory and confirmation that no active run needs those files.
Do not infer that ignored runtime storage can replace durable task evidence.

## Validation

The [runtime validation record](validation.json) retains check commands, outcomes, and original log hashes.
Large text logs use lossless gzip storage. Original byte hashes and compressed hashes remain separate.
The complete Python suite ran 883 tests: 881 passed and two existing optional integrations skipped.
No test failed and no runner error remained during approved local execution.
The first sandbox attempt had 36 socket-binding errors. Its [original output](python-tests-sandbox.log.gz) remains available.
Those environment errors did not establish product defects.

The wheel build and both workspace validations passed.
A workspace initialized from the built wheel retained four updated guides with matching bytes.
It contained no project task contents.
Added Markdown links, the skill validator, and the diff checks passed.

The [E2E validation record](validation-e2e.json) covers 29 unit tests, 32 consumer tests, and two browser integration tests.
TypeScript checks also passed.
The browser probe uses one passing case and one deliberate failure to check capture disposition.
Its deliberate failure is a probe input. The integration test asserts that outcome and passes.
The probe checks retained references after runner exit, screenshots, manifest hashes, and explicit capture modes.
These are controlled harness checks. They do not establish business behavior or production execution.
Native Windows execution remains untested.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
