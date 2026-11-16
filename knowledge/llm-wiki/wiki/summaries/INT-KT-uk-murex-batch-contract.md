---
type: Summary
description: "Preserves UK Murex payment bands, batch-file sequencing, exception variants, and unresolved replay behavior."
doc_type: short
full_text: sources/INT-KT-uk-murex-batch-contract.md
---

> **Candidate/draft only:** These UK feed and batch descriptions lack an effective version and completed execution evidence. Owner is unknown; `verified` is empty.

# UK Murex batch payment contract

The functional proposal separates real-time MxML payments for T−1 through T+1 business days from CSV batches for T+2 through T+7, excluding weekends and two listed holidays. A batch uses Base, Snapshot, and Completion files, with sequence and count fields. An `_END.csv` is required even when no batch runs. Murex waits for an Ack/Nack file before the next batch; a 30-minute timeout holds processing for investigation.

File-level failures stop the batch and later batches; payment-level failures allow the batch to continue. The functional design names one set of exceptions and leaves payment responses and replay TBC. The technical sketch proposes two-hour batches, a 45,000-record limit, different exception names, and a different retry boundary. A separate H2 DOI gives a 6,000-payment limit. The sources do not reconcile timezone, capacities, or effective version.

The related [[summaries/INT-KT-murex-ratan-feed-lifecycle]] has other Murex feed windows and cohorts. Those windows must remain scoped to their own source revisions.

## Canonical sections

- [INT-BATCH-01 — UK payment bands and file contract](../../../records/candidates/settlement/INT-KT-uk-murex-batch-contract.md#int-batch-01--uk-payment-bands-and-file-contract)
- [INT-BATCH-02 — UK file exception distinctions](../../../records/candidates/settlement/INT-KT-uk-murex-batch-contract.md#int-batch-02--uk-file-exception-distinctions)
- [INT-BATCH-03 — Technical batch design and unresolved contract differences](../../../records/candidates/settlement/INT-KT-uk-murex-batch-contract.md#int-batch-03--technical-batch-design-and-unresolved-contract-differences)

## Related candidate topics

- [[summaries/KT-settlement-feeds-p3]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
