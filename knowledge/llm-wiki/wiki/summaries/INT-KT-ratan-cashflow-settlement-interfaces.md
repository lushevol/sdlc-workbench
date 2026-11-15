---
type: Summary
description: Summarizes selected RATAN accounting, cashflow, settlement, and SSI interfaces while preserving route uncertainty.
doc_type: short
full_text: sources/INT-KT-ratan-cashflow-settlement-interfaces.md
---

> Derived from [candidate record version 1](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md). Owner review and publication remain pending.

# RATAN cashflow and settlement interfaces

The candidate groups source-described interfaces across 12 selected pages. Each pair has its own messages, scope, dates, and operating conditions. The sources establish no current approved contract or deployment. [Scope](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#scope) [Evidence limits](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#evidence-limits)

## Accounting and reporting

Aspire uses a FileIT payment-accounting batch. EBBS describes real-time JSON accounting over Solace for listed entities. The Korea OLTP design describes accounting through KREDMI and FM Solace. [Selected accounting flows](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#payment-accounting-and-downstream-reporting)

The TLM query is limited to Korea entity `10036645`, records with status `SENT`, and a three-day maximum window. FMMIS, CIS, PacMan, MarketUDP/SSDR, and CNEDMp query RATAN cashflows through REST APIs. [TLM and query scope](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#payment-accounting-and-downstream-reporting)

## Cashflow and settlement processing

Murex describes MQ delivery for T−1 through T+1 and SFTP batches for T+2 through T+7. Corrective files use SFTP regardless of value date. The source excludes weekends and public holidays from batch delivery. [Murex cashflow windows](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing)

The Murex page says transfers wait for RATAN ACK or NACK. A missing response for 30 minutes holds processing for Murex PSS investigation. FMSGW, Razor, and FXU describe separate settlement, feed, and utilization flows. [Murex response and related flows](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing)

SSI+ supplies SSI data through its API and sends record-change notifications over Solace. The candidate records distinct monitoring responsibilities for SSI+ PSS and RATAN PSS. [SSI+ flow and support](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing)

## Korea ENISIS transport remains unresolved

The Murex KR page describes SFTP for MX messages to ENISIS. The ENISIS page describes FM Solace for MX and MT210 messages. The selected pages do not explain the difference by message, stage, or design revision. [Both source descriptions](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing) [Open question](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#open-questions)

The candidate preserves both routes and source-described recovery steps. It does not choose a current Korea transport. The proposed ENISIS exception blotter has no confirmed build or operating status.

## Related topics

- [[summaries/KT-settlement-korea-trade-confirmation|Korea COMP confirmation]] covers the separate payment confirmation gate.
- [[summaries/KT-settlement-lms-feed|LMS feed]] covers payment-feed eligibility and payload proposals.
- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back|Cashflow identity]] covers identity and status write-back questions.
- [[summaries/KT-settlement-auto-netting|Auto-netting]] covers netting rules and outcomes.
