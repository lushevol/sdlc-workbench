---
type: Summary
description: "Collects candidate regional payment-message mappings and their incomplete or conflicting fields."
doc_type: short
full_text: sources/KT-settlement-regional-swift-customization.md
---

# Regional SWIFT customization conditions

> **Source status:** Candidate/draft. These historical regional mappings do not establish current message contracts.

The source records conditional country and currency rules. India INR NOS payments at or above 500 million require sender and counterparty LEI in MT103 field 70 or MT202 field 72. Egypt RTGS NOS changes receiver BIC and correspondent account by message type; its camt.057 and camt.058 conditions contain inconsistent entity FMID text. Precious-metal routing uses enumerated entities and currencies. Dubai AED NOS MT103 and cover flows use 26T TOF; Dubai non-AED MAIN NOS payments have a separate 77B purpose condition. [Conditional regional mappings](../../../records/candidates/settlement/KT-settlement-regional-swift-customization.md#conditional-regional-payment-mappings)

Other entries retain material gaps: UK GBP purpose/LEI rules repeat sender predicates without specifying target paths; KWD names a currency without a complete mapping. Hong Kong same-BIC pacs.008 uses local instrument FMS; Thai internal payments preserve SPRO on line 1; Vietnam excludes 202COV from a described MX rebuild; HAU MT604/605 varies commodity instructions by PVP conditions. [Regional MX and commodity conditions](../../../records/candidates/settlement/KT-settlement-regional-swift-customization.md#regional-mx-and-commodity-conditions)

Confirm authoritative versions and field-level contracts before use. Related regional proposals: [[summaries/INT-KT-indonesia-regional-architecture]].
