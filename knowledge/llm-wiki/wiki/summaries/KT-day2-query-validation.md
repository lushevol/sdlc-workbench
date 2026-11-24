---
type: Summary
description: "Summarizes candidate query predicates, operator limits, invalid-filter handling, and UI conditions."
doc_type: short
full_text: sources/KT-day2-query-validation.md
---

# Quick-search and custom-filter validation

> **Source status:** Candidate/draft. This retained requirement proposal has unknown current authority and applicability.

The source bypasses validation for trade original-ID queries. Other described searches require value date and either booking entity or counterparty. Payment date accepts `=`, `in`, `bet`, `<=`, and `>=`; booking-entity FMID and cashflow state accept `=` and `in`. Multiple cashflow states require no additional field validation. [Bounded query validation](../../../records/candidates/query/KT-day2-query-validation.md#l3-query-01--bounded-query-validation)

Opening an invalid saved filter should warn while keeping it visible. [L3-QUERY-01](../../../records/candidates/query/KT-day2-query-validation.md#l3-query-01--bounded-query-validation) Invalid filters cannot be saved, created, or searched; deletion remains allowed. Query or filter searches disable and clear the search bar. Navigation buttons highlight on first click and toggle off on the next; the Today value follows that behavior. Cashflow Sub State remains conditional on user confirmation, which this record does not supply. [Search UI controls](../../../records/candidates/query/KT-day2-query-validation.md#l3-query-02--search-ui-controls) [Open question](../../../records/candidates/query/KT-day2-query-validation.md#open-questions)

The source does not establish implementation or acceptance. Confirm the validation scope, operators, user messages, and Sub State decision before applying these rules. Related: [[summaries/ARC-platform-cashflow-data-query]].
