# Runtime accounting review

## Findings

### P2 Bind declared existing coverage to retained canonical output hashes

Candidate location is `core/ingestion/incremental.py` at `bf0f10a09`, lines 86–90.
The added validator accepts any nonempty `target` for `existing_coverage`.
Completion and planning only bind paths supplied through `outputs`, source citations, and existing graph relationships.
Accounting targets never enter that dependency calculation.

A source completed with `outputs=[]` and a nonexistent canonical target returned `COMPLETED`.
Its next plan reported one unchanged source and an empty processing queue.
A second probe used a real canonical target owned by another source.
Changing and deleting that target queued its owning source while skipping the source claiming existing coverage.
The skipped receipt contained empty `outputs` and `input.dependencies` objects.

The source-preparation contract requires a canonical record path for existing coverage.
The probes establish missing identity and freshness binding.
They make no claim about automated semantic truth.

Owner is unknown.
Resolve declared existing-coverage targets and bind their current hashes through outputs or dependencies.
Keep contextual and redundant zero-output completions available.
Verify that target edits and deletion requeue each dependent source.

Evidence files are `unbound-target.json`, `target-staleness.json`, and `probe.py` beside this report.
Supporting code is `_scope`, lines 262–272, and `complete_sources`, lines 467–487.
The reference contract is `.agents/skills/ingest-knowledge/references/source-preparation.md`, lines 199–209.

### P2 Document the newly required no-change JSON shape

Candidate location is `core/ingestion/incremental.py` at `bf0f10a09`, lines 82–91.
The command now requires `review.source_to_output` and four exact keys per item.
The accepted disposition values are three underscore-separated enum strings.
The shipped source-preparation reference supplies the previous review-note JSON shape and a prose accounting table.
It never shows the required property, item keys, or enum spellings.

The probe populated that documented review-note shape with a source range, contextual disposition, and supporting reason.
The baseline accepted the no-change completion.
The candidate rejected the same shape with `A no-change review requires source-to-output accounting.`
An installed-workspace user following the documented result contract cannot complete this supported outcome without inspecting runtime source.

Owner is unknown.
Add a working no-change results example and explain required field names and supported values.
Exercise that published example through the normal CLI in the installed-workspace smoke check.

Evidence is `documented-review.json` and `probe.py` beside this report.
The unchanged reference locations are lines 180–184 and 199–209.

### P3 Validate types before new membership expressions

Candidate locations are `core/ingestion/incremental.py` at `bf0f10a09`, lines 88 and 153–154.
The new receipt argument checks membership in `receipt["review"]` before `_review` validates its type.
A receipt with `review=null` previously produced a structured `WorkbenchError`.
The candidate raises an uncaught `TypeError` through the public `sources plan` CLI.
A JSON-compatible `disposition=[]` in accounting similarly raises `TypeError` during set membership.
The CLI catches `WorkbenchError` and `OSError`, leaving these failures uncaught.

Owner is unknown.
Validate review and disposition types before membership operations.
Verify that malformed JSON-compatible inputs produce structured errors without changing receipts.

Evidence is `legacy-review.json`, `malformed-accounting.json`, and `probe.py` beside this report.
The CLI error boundary is `core/cli.py`, lines 422–433.

## Comparison and checks

- Base commit is `af8f2af752756a910bcd18d019d947df8dd3ec65`.
- Candidate commit is `bf0f10a09b525e6beb53dd2e6cda7a2257837127`.
- Comparison fingerprint is `07b47075b7ec427bb0bbe6e446dca5914441e349c75da48026ac5a974a5cebfc`.
- The probe and suite pin runtime, CLI, and test modules to the selected candidate bytes.
- The source-preparation reference matches the selected candidate.
- Concurrent parent edits changed runtime and tests during the final worktree check.
- Pinned reruns passed all candidate cases and all 32 candidate tests.
- All five changed files were inspected, including the retained evaluation JSON.
- The focused ingestion, CLI, and layout suite passed all 32 tests.
- New missing and pending accounting rejection tests passed.
- A valid legacy receipt without accounting requeued with `source_to_output_accounting_missing`.
- The existing test suite does not cover unbound targets or the malformed input cases above.
- `context.json`, `scan.json`, `focused-tests.log`, `pinned-tests.log`, and `source-manifest.json` retain command and source evidence.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_incremental_ingestion tests.test_source_preparation_cli tests.test_knowledge_layout -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python /tmp/runtime-accounting-review-20261117/pinned-tests.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python /tmp/runtime-accounting-review-20261117/probe.py
```

## Limits

All probes used synthetic local fixtures and the installed editable package.
The baseline probe loaded the exact previous runtime module against the same fixture dependencies.
The focused suite also exercised the consolidated knowledge layout.
Full-package tests, wheel initialization, publication, and remote systems remain outside this review scope.
Semantic completeness and reviewer authority remain review responsibilities.
Repository files were left untouched.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks cover source identity and focused behavioral assertions.
  - Automated checks do not establish complete writing review.
```
