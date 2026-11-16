---
type: Summary
description: "Summarizes proposed SSI+ Nostro centralization, upload, and RFI stamping behavior while retaining technical and functional conflicts."
doc_type: short
full_text: sources/KT-day2-nostro-centralization-and-rfi.md
---

> **Candidate/draft only:** SSI+ interfaces, RFI selection rules, migration, and current applicability remain unconfirmed.

# Nostro Centralization and Dedicated RFI Selection

The centralization proposal assigns Data Ops maintenance to SSI+ and asks RATAN to refresh cashflow, trade, and accounting Nostro data after New, Update, or Delete events. Event schemas, field mapping, and migration of historical cashflow-linked Nostro IDs remain open.

The CSV-upload proposal rejects the whole file when content is invalid. It names a duplicate key across legal entity, currency, settlement means/account, and date range, but does not specify operator authorization. Dedicated lookup selects memory plus database, with a child table for dedicated data; new Nostro types still require code and mapping changes.

The RFI functional proposal queries by booking entity, currency, and portfolio: one match stamps, multiple matches raise Missing Nostro, and no match follows ordinary stamping. Technical questions conflict on no-match fallback, Vostro/Nostro mismatch, lookup entry points, KRO/KOR literals, uniqueness fields, and existing-record migration. Retain these alternatives until owners confirm the effective contract.

## Canonical sections

- [L3-NOSTRO-01 — Centralization target](../../../records/candidates/settlement/KT-day2-nostro-centralization-and-rfi.md#l3-nostro-01--centralization-target)
- [L3-NOSTRO-02 — Atomic CSV import proposal](../../../records/candidates/settlement/KT-day2-nostro-centralization-and-rfi.md#l3-nostro-02--atomic-csv-import-proposal)
- [L3-NOSTRO-03 — Dedicated lookup architecture](../../../records/candidates/settlement/KT-day2-nostro-centralization-and-rfi.md#l3-nostro-03--dedicated-lookup-architecture)
- [L3-NOSTRO-04 — Conflicting technical decisions](../../../records/candidates/settlement/KT-day2-nostro-centralization-and-rfi.md#l3-nostro-04--conflicting-technical-decisions)
- [L3-NOSTRO-06 — Functional RFI selection and exceptions](../../../records/candidates/settlement/KT-day2-nostro-centralization-and-rfi.md#l3-nostro-06--functional-rfi-selection-and-exceptions)


## Related candidate topics

- [[summaries/KT-ratan-nostro-golden-source-proposal]]
- [[summaries/KT-day2-ssi-validation-and-selection]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
