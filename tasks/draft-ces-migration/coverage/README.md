---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Run CES migration coverage

> **The default launcher verifies supplied mock responses; complete migration parity remains unassessed.**
> Action: review the [mock report](../evidence/coverage-runs/mock-supplied-20261103/report.html) and its unavailable-account counts.
> Consequence: two paired user examples cannot establish equality for the complete account population.
> Owner: unknown. Source: [mock execution boundary](../evidence/coverage-mock-20261103/user-input.md#exact-user-input).

## Configure once

Use the installed Workbench Python environment. No additional spreadsheet package is required.
Edit [config.json](config.json) for entity/application mappings, source workbooks, endpoints, and output location.
EMS2 role/entity/subject/action map to CES entitlement/application/feature/action.
Optional `role_mapping`, `subject_mapping`, and `action_mapping` entries provide explicit name translations within each EMS2 entity.
Keep FMO Portal Admin `included: false`: its non-production comparison has lower priority and a separate scope reason.

The default mock run needs no credentials, certificate file, or enterprise network access.
It reads the response bodies supplied in the configured API example files.
It does not load private `.env` credentials or construct an HTTP client.

## Run both checks

On macOS, double-click [run-coverage.command](../run-coverage.command).
On Windows, double-click [run-coverage.cmd](../run-coverage.cmd).
Each launcher runs supplied-response replay and opens the HTML result.
The report labels this execution as mock verification.
Set `CES_COVERAGE_PYTHON` to select another Python environment with Workbench installed.

From the Workbench root, the equivalent command is:

```sh
.venv/bin/python -m ai_sdlc_workbench.entitlement_coverage --config tasks/draft-ces-migration/coverage/config.json --open
```

The explicit equivalent is:

```sh
.venv/bin/python -m ai_sdlc_workbench.entitlement_coverage --config tasks/draft-ces-migration/coverage/config.json --mode replay --open
```

Replay verifies only the retained examples. Uncaptured accounts remain unassessed in the complete discovered population.
Resume a retained run with the same configuration, implementation, matrix, mode, and applicable replay-source hashes:

```sh
.venv/bin/python -m ai_sdlc_workbench.entitlement_coverage --config tasks/draft-ces-migration/coverage/config.json --resume tasks/draft-ces-migration/evidence/coverage-runs/RUN-DIRECTORY --open
```

Replace `RUN-DIRECTORY` with the actual retained run folder. Changed bindings require a new run.
An optional `--user-limit N` bounds diagnostics. Remaining accounts stay unassessed and do not establish final coverage.
Missing or invalid stored responses remain unassessed. Replay does not fabricate permission responses for uncaptured accounts.

## Read the output

Each new run writes a timestamped folder under `tasks/draft-ces-migration/evidence/coverage-runs/`.

| File | Purpose |
| --- | --- |
| `report.html` | Coverage summary, source limits, and active differences. |
| `result.json` | Complete counts, matched content, differences, account outcomes, and source bindings. |
| `differences.csv` | Missing, additional, inconsistent, and unassessed items for review. |
| `cases.jsonl` | Durable account checkpoints, written as comparisons complete. |
| `responses/` | Retained response data with request identities and hashes. |
| `binding.json` | Configuration, implementation, matrix, and replay identities for recovery. |

Matched records remain in JSON and coverage totals. HTML and CSV omit their detailed rows from the active differences.
Only explicitly configured `excluded_features` classify CES administration scope separately.
Unknown features and additional `Reports` or `FMID Reports` permissions stay visible for review.
Exit codes are `0` for functional agreement, `1` for differences, and `2` for incomplete collection or setup failure.

## Interpret the scope

The supplied inputs contain 747 production-matrix accounts and 1,050 CES catalog accounts, with 1,051 distinct combined IDs.
These are observed input counts, recalculated dynamically each run, not a fixed account list.
The runner compares the combined population against available stored responses. Baseline coverage uses the EMS2 account population.
Available EMS2 responses can add discovered baseline accounts beyond the initial matrix inventory.
No complete EMS2 account-directory endpoint was supplied. Accounts absent from both discovery sources remain outside demonstrated discovery coverage.
Unavailable comparisons remain unassessed. The final functional coverage rate stays `null` until the baseline is completely assessed.
Full data-profile equality remains unassessed without comparable authoritative EMS2 field/value definitions.
Catalog definitions, effective grants, and reconstructed role provenance remain separate evidence.
Captured timestamps do not establish an atomic synchronization snapshot across EMS2 and CES.

## Explicit live mode

`--mode live` remains available for a separately authorized environment with valid credentials and trusted TLS.
It is outside the current [mock-only execution boundary](../evidence/coverage-mock-20261103/user-input.md#exact-user-input).
Only live mode reads private environment references and constructs HTTP clients.
The earlier [TLS preflight](../evidence/coverage-runs/live-access-check-unsandboxed/result.json) remains historical evidence.
No enterprise connection is needed to run or verify the current default workflow.
