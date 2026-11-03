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

> **Enterprise collection requires working TLS trust and authorized access.**
> Action: configure the trusted certificate chain and current private credentials, then rerun live collection.
> Consequence: the retained [live preflight](../evidence/coverage-runs/live-access-check-unsandboxed/result.json) reports `TLS_ERROR`; enterprise account parity remains unverified.
> Owner: unknown. Source: [coverage request](../evidence/coverage-automation-20261103/user-input.md#exact-user-input).

## Configure once

Use the installed Workbench Python environment. No additional spreadsheet package is required.
Edit [config.json](config.json) for entity/application mappings, source workbooks, endpoints, and output location.
EMS2 role/entity/subject/action map to CES entitlement/application/feature/action.
Optional `role_mapping`, `subject_mapping`, and `action_mapping` entries provide explicit name translations within each EMS2 entity.
Keep FMO Portal Admin `included: false`: its non-production comparison has lower priority and a separate scope reason.

Set private values in the ignored Workbench root `.env`, or export process environment variables.
Process values override `.env` values, including explicit empty values.

```dotenv
CES_COVERAGE_BEARER_TOKEN=your-current-CES-token
CES_COVERAGE_EMS2_TOKEN=your-EMS2-token-if-required
CES_COVERAGE_CA_FILE=/absolute/path/to/trusted-enterprise-ca.pem
```

The EMS2 token and custom CA file are optional when the environment does not require them.
Relative CA paths resolve from the Workbench root. TLS certificate validation stays enabled.
The runner reads credentials through environment references and redacts credential fields from retained responses.

## Run both checks

On macOS, double-click [run-coverage.command](../run-coverage.command).
On Windows, double-click [run-coverage.cmd](../run-coverage.cmd).
Each launcher runs live collection and opens the HTML result.
Set `CES_COVERAGE_PYTHON` to select another Python environment with Workbench installed.

From the Workbench root, the equivalent command is:

```sh
.venv/bin/python -m ai_sdlc_workbench.entitlement_coverage --config tasks/draft-ces-migration/coverage/config.json --open
```

Use stored API examples without network access:

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
Global authentication, network, or TLS failures stop further account scheduling after the current batch finishes.

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
The combined population is fetched to expose target-only grants. Baseline coverage uses the EMS2 account population.
Acquired EMS2 permissions can add discovered baseline accounts beyond the initial matrix inventory.
No complete EMS2 account-directory endpoint was supplied. Accounts absent from both discovery sources remain outside demonstrated discovery coverage.
Unavailable comparisons remain unassessed. The final functional coverage rate stays `null` until the baseline is completely assessed.
Full data-profile equality remains unassessed without comparable authoritative EMS2 field/value definitions.
Catalog definitions, effective grants, and reconstructed role provenance remain separate evidence.
Captured timestamps do not establish an atomic synchronization snapshot across EMS2 and CES.
