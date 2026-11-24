---
type: Summary
description: "Preserves Indonesia RDM compensation and rule-synchronization proposals, including distinct API, timing, eligibility, and retry rules."
doc_type: short
full_text: sources/INT-KT-indonesia-reference-data-and-rule-sync.md
---

> **Candidate/draft only:** Endpoint, synchronization, security, and timing proposals have no confirmed current approval or execution evidence.

# Indonesia Reference-Data and Rule Synchronization

The Indonesia design selects EOD API compensation for holiday and country data because NAS mounting is unavailable. It states an inclusive/exclusive date interval, different page-number starts for holiday and country endpoints, and different date formats between API and real-time feeds. Holiday keys use center, date, name, and file type; RDM describes key changes as deletion, while the RATAN note says insert/delete. The schedule uses “after 8am IST,” whose timezone is undefined.

The Kong table distinguishes SIT, UAT, and PROD endpoint families. Its literal currency URL has two question marks; the summary preserves that syntax rather than silently correcting it.

Rule-sync eligibility replaces manual checkboxes with automatic detection for selected strategic-settlement rule types. Global rules are read-only in Indonesia; Indonesia-specific rules include locked Indonesia predicates. The rule service and generic static synchronizer have different timeout, IGNORE, and retry descriptions. Proposal A is one-way FM Solace copying; the alternative is incomplete. No delivery guarantee or approved security policy is established.

## Canonical sections

- [SYNC-01 — Indonesia RDM compensation choice](../../../records/candidates/settlement/INT-KT-indonesia-reference-data-and-rule-sync.md#sync-01--indonesia-rdm-compensation-choice)
- [SYNC-02 — RDM Kong interface distinctions](../../../records/candidates/settlement/INT-KT-indonesia-reference-data-and-rule-sync.md#sync-02--rdm-kong-interface-distinctions)
- [SYNC-03 — Rule synchronization eligibility and controls](../../../records/candidates/settlement/INT-KT-indonesia-reference-data-and-rule-sync.md#sync-03--rule-synchronization-eligibility-and-controls)
- [SYNC-04 — Rule request lifecycle](../../../records/candidates/settlement/INT-KT-indonesia-reference-data-and-rule-sync.md#sync-04--rule-request-lifecycle)
- [SYNC-05 — Generic static synchronizer](../../../records/candidates/settlement/INT-KT-indonesia-reference-data-and-rule-sync.md#sync-05--generic-static-synchronizer)


## Related candidate topics

- [[summaries/KT-static-data-cache-p3]]
- [[summaries/KT-ratan-settlement-integration-checklist-scope]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
