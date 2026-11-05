# Task evidence growth review

**Future audit runs reuse canonical trace payloads. Historical evidence still requires a scoped cleanup review.**
Owner: Workbench maintainers.
Consequence: repeated captures consume disk and increase review work.
Evidence: [measured files](measurements.json) and [audit capture configuration](../../../e2e/audit.config.ts).

The [user input](user-input.md#exact-user-input) defines this maintenance scope.
This review changes capture behavior and shared procedures. It does not delete historical evidence.

## Measured scope

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

The original [audit configuration](../../../e2e/audit.config.ts) enabled traces for every test.
The [audit reporter](../../../e2e/audit.reporter.ts) copied attachments from durable run storage into each case.
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
The revised [growth controls](../../../tasks/README.md#control-evidence-growth-before-execution) establish one canonical payload and shared run bindings.

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
