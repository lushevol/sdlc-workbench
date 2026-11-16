---
type: Summary
description: "Summarizes candidate Global Rates ownership, event, booking, and settlement-method proposals."
doc_type: short
full_text: sources/KT-settlement-global-rates-design-boundaries.md
---

# Global Rates settlement design boundaries

> **Source status:** Candidate/draft. These strategy and feature notes contain proposals, not approved or verified behavior.

The strategy asks Blade or Stella to stamp settlement method on trades and cashflows. A later settlement-method amendment remains required, but its operating solution is unresolved. The DVP proposal holds payments until receipt settlement confirmation. Shared rounding, identifiers, currencies, and product classification need aligned source ownership. CLS, PVP, netting agreements, LIEN, rollover, and utilization still contain unanswered design questions. [Global Rates target responsibilities](../../../records/candidates/settlement/KT-settlement-global-rates-design-boundaries.md#global-rates-target-responsibilities)

A separate inventory proposes distinct Clearing and Remaining Party Full events. Allocation block trades generate SUSPENDED cashflows; child trades generate PROJECTED cashflows. Refresh represents calendar-driven amendment behavior, while step-in events are described as new bookings. Deliverable-currency and ND-convert features still need product and currency scope. “No Dev” and “Only UAT” labels do not prove conformance or execution. [Event and booking proposals](../../../records/candidates/settlement/KT-settlement-global-rates-design-boundaries.md#event-and-booking-proposals) [Open questions](../../../records/candidates/settlement/KT-settlement-global-rates-design-boundaries.md#open-questions)

Confirm current scope, event contracts, golden sources, and amendment design. Related: [[summaries/ARC-settlement-platform-p3]] and [[summaries/KT-settlement-auto-netting]].
