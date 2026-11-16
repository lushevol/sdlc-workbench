---
type: KnowledgeTopic
id: INT-KT-uk-murex-batch-contract
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-97fdce8330e2bfa135f8d2b6
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Surrounding System Integration/UK - Murex -  RATAN cashflow feeding/page.md
  revision: sha256:adf12d24386ece86835635d31d42762e2621c2cde5c83d4316084a406508b52a
  sha256: adf12d24386ece86835635d31d42762e2621c2cde5c83d4316084a406508b52a
- id: SRC-ca5bac3c10527815ef86dde4
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Murex
    batch processing/page.md
  revision: sha256:0151166eeb599d2368378e0e1963783e150b62b6430e1d19104bdabebf4bc6b3
  sha256: 0151166eeb599d2368378e0e1963783e150b62b6430e1d19104bdabebf4bc6b3
generated:
  by: agent:codex:sol-integrations-review
  at: '2026-11-16T01:17:44.322603+00:00'
verified: []
classification: settlement
scope: UK Murex batch payment contract
summary: Selected source descriptions preserve scoped intended responsibilities. Current
  authority and applicability remain unresolved.
related:
- INT-KT-murex-ratan-feed-lifecycle
- INT-KT-ratan-cashflow-settlement-interfaces
open_questions:
- 'KDQ-87bea04f8a: Which timezone, endpoint inclusivity, batch capacity, and effective
  version govern each UK feed band?'
- 'KDQ-1001eb4636: Which payment validation response and stable exception names are
  approved?'
- 'KDQ-b25e634774: Who authorizes replay after batch NACK or timeout, and how must
  reconciliation finish before restart?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# UK Murex batch payment contract

## Scope

UK Murex batch payment contract.
These source descriptions define separate contracts. They establish no deployed or tested behavior.

## Summary

The selected sources describe related responsibilities and conditions.
Their original authority, effective dates, and current applicability remain unresolved.

## Documented knowledge

### INT-BATCH-01 — UK payment bands and file contract

The UK proposal separates individual MxML payments from CSV batches; the two feeds must not overlap.
Real-time input covers T-1, T, and T+1 business days. CSV covers T+2 through T+7, excluding weekends, 25 December, and 1 January.
Each batch has Base, Snapshot, and Completion files.
Names use `FMRP_Murex_Payments_YYYYMMDD_XXX_Base.csv`, corresponding `_Snapshot.csv`, and `_Completion_ZZZZ.csv`.
`XXX` is the daily batch sequence; `ZZZZ` is the Base payment count for reconciliation.
An `_END.csv` file is mandatory even when no batch ran.
The Base has fixed column names and order. Snapshot processing uses CNCL and SNTR, and ignores INIT.
Murex waits for the RATAN Ack or Nack file before processing the next batch.
Without a response for 30 minutes, processing holds for Murex PSS investigation.
NACK requires RATAN PSS escalation to Murex PSS.
File errors stop the batch and subsequent batches. Payment errors let the batch continue and raise a payment exception.
The detailed payment-error display and action remain TBC.

[Selected original evidence](../../../evidence/sources/sha256/adf12d24386ece86835635d31d42762e2621c2cde5c83d4316084a406508b52a.md#L1-L14).

### INT-BATCH-02 — UK file exception distinctions

The functional proposal names `BatchFileNotComplete`, `BatchReconError`, and `BatchFormatError`.
These apply to missing files, payment-count mismatch, and incorrect columns or order.
It names `BatchDateNotEnd` when batch 001 arrives before the previous ending file.
The receiver holds batch 001 while awaiting that ending file.
Missing batch 002 raises no exception; the join repeats until its completion file arrives.
Expected Murex replay and resend actions are explicitly TBC.
`PaymentValidationError` covers missing or invalid fields and Base payments missing from Snapshot; response behavior remains TBC.

[Selected original evidence](../../../evidence/sources/sha256/adf12d24386ece86835635d31d42762e2621c2cde5c83d4316084a406508b52a.md#L14).

### INT-BATCH-03 — Technical batch design and unresolved contract differences

The technical sketch proposes batches every two hours from `00:00:00` through `19:00:00`. It gives no timezone.
Each batch sends Snapshot and Base, followed by a completion file after upload.
The proposed Base limit is 45,000 records; Base contains SNTR only.
It names `BatchFileFormatError` and `BatchCountReconError`, unlike the functional proposal's labels.
Both stop the current and subsequent files until Murex republishes the current batch.
Its `PaymentValidationError` stops one record until the payment is republished.
This technical proposal does not resolve the functional page's TBC response.
The separate H2 DOI uses 6,000 distant-date payments per two-hour run. It supplies a different version and scope, not an equivalent 45,000-record contract.

[Selected original evidence](../../../evidence/sources/sha256/0151166eeb599d2368378e0e1963783e150b62b6430e1d19104bdabebf4bc6b3.md#L1-L20).

## Connections

Related canonical IDs: `INT-KT-murex-ratan-feed-lifecycle`, `INT-KT-ratan-cashflow-settlement-interfaces`.

## Evidence limits

Source descriptions supply documented intent and historical proposals only.
They do not establish current approval, implementation, configuration, deployment, execution, or acceptance.
Unselected content and attachments were not used to fill gaps.

## Open questions

Owner: unknown. Answers remain pending in the single [task question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
