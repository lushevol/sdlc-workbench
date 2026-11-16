---
type: Summary
description: "Summarizes source-specific RATAN reference, control, valuation, confirmation, and TIS interface responsibilities."
doc_type: short
full_text: sources/INT-KT-ratan-reference-and-control-interfaces.md
---

# RATAN reference and control interface responsibilities

> **Source status:** Candidate/draft. Interfaces are source-described responsibilities; no current deployment or runtime connectivity is established.

The record assigns different responsibilities to Apollo, SCI/DQSL, BRDM, CDUPS, Falcon, Markets UDP, RDM, TDS3, TDSX, and MDS. Examples include rule validation, counterparty enrichment, bank-code and holiday feeds, trade confirmation, valuation input, and reference-data delivery. Their routes, schedules, and source systems remain distinct. [INT-RC-01](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#int-rc-01--apollo-validation) [INT-RC-04](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#int-rc-04--cdups-stamping-and-confirmation) [INT-RC-08](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#int-rc-08--tds3-trade-and-settlement-responsibilities)

A proposed TIS retrieval scope is limited to Released or Settled NOX cashflows, no reversal event, and entity FMID `10036645`; it disallows SSI updates after release. The Korea guide adds payment-code, beneficiary-account, endpoint, and exception-handling descriptions. Its OLTP exclusion differs from another NOS/selected-NOX allowlist, so current precedence is unresolved. [INT-RC-11](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#int-rc-11--proposed-tis-payment-retrieval) [KR-DOI](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#kr-doi--korea-tis-and-downstream-operating-contract)

The material includes schedules, identifiers, and API details but omits approval, schema completeness, and execution evidence. TIS pagination, authorization, and response contracts are not defined. Preserve unresolved clock pairs and placeholder URLs. [INT-RC-06](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#int-rc-06--markets-udp-valuation-coordination) [Evidence limits](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#evidence-limits)

See [[summaries/ARC-settlement-platform-p3]] and [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]] for adjacent interface context.

## Subscriber and literal timing boundaries

The catalog assigns CDU-IS subscription to RATAN trade messages for confirmation. This responsibility accompanies the separate stamping, confirmation, and outbound information flows. [Canonical detail](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#cdups-subscriber-responsibility)

The three literal feed-to-exception pairs are 15:00/16:00 SGT, shown as 06:00/07:00 UTC; 15:00/16:00 UKT, shown as 14:00/15:00 UTC; and 15:00/16:00 UST, shown as 18:00/19:00 UTC. The SGT inconsistency and UKT/UST clock profiles remain unresolved. Historical expected times establish no current service guarantee. [Canonical detail](../../../records/candidates/settlement/INT-KT-ratan-reference-and-control-interfaces.md#literal-markets-udp-intraday-timing-catalog)
