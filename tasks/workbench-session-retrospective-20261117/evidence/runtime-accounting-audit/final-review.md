# Runtime accounting correction re-review

**PASS** for the bounded runtime-accounting correction.
No actionable defect remains in the reviewed scope.

The comparison starts at `bf0f10a09b525e6beb53dd2e6cda7a2257837127` and ends at the verified worktree hashes below.
Original adverse evidence remains beside this report.

## Corrected findings

| Original finding | Verified result |
| --- | --- |
| Existing coverage lacked target binding. | Domain targets require output membership and section locators. Output hashes requeue sources after edits or deletion. |
| Required accounting JSON lacked a documented shape. | The new published example completed through the public CLI and supported an idempotent retry. |
| Malformed declarations escaped structured error handling. | Malformed review objects and accounting dispositions now produce supported errors. |
| Navigation targets bypassed freshness binding during correction review. | New navigation coverage is rejected. Historical navigation receipts remain readable, unchanged, and queued. |

## Independent checks

- All 36 focused ingestion, source-preparation CLI, and knowledge-layout tests passed.
- The documented existing-coverage example returned `COMPLETED` through `sources complete`.
- Its identical CLI retry wrote zero receipts.
- Its next CLI plan counted one unchanged source.
- Navigation-target completion failed before writing any receipt.
- A historical navigation receipt requeued with `source_to_output_accounting_missing`.
- Reading that historical receipt preserved its exact bytes.
- The reviewed source hashes remained stable through the probes and focused suite.
- The scoped `git diff --check` passed.

Commands and results are retained in `final-validation.py`, `final-validation.json`, and `final-focused-tests.log`.
The selected diff is retained in `final-reviewed.diff`.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python /tmp/runtime-accounting-review-20261117/final-validation.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_incremental_ingestion tests.test_source_preparation_cli tests.test_knowledge_layout -v
git diff --check -- core/ingestion/incremental.py tests/test_incremental_ingestion.py .agents/skills/ingest-knowledge/references/source-preparation.md
```

## Reviewed source hashes

| Path | SHA-256 |
| --- | --- |
| `core/ingestion/incremental.py` | `238345c533498c064e89ef3a7aa55b1bd6b30356130464bef2ae06eac3ca858d` |
| `tests/test_incremental_ingestion.py` | `b40a63241f07e86aec7f1f9026739376eaa23cba2993ad278e20bef7d8c43de5` |
| `.agents/skills/ingest-knowledge/references/source-preparation.md` | `7fc944c299a5df3d287af02a38a9a99721ca6252ba5f8cf440c74f62fcbf8524` |

## Limits

Tests used synthetic local fixtures and the editable runtime package.
Semantic source support, section meaning, completeness, and reviewer authority require substantive review.
Full-package tests, wheel initialization, publication, and remote behavior remain outside this independent review scope.
This reviewer made no repository edits.

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
