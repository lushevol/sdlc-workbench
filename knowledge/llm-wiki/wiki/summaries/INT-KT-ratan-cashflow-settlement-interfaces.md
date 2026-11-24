---
type: Summary
description: Summarizes selected RATAN accounting, cashflow, settlement, and SSI interfaces while preserving route uncertainty.
doc_type: short
full_text: sources/INT-KT-ratan-cashflow-settlement-interfaces.md
---

> Derived from [candidate record version 2](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md). Owner review and publication remain pending.

# RATAN cashflow and settlement interfaces

The candidate groups source-described interfaces across 12 selected pages. Each pair has its own messages, scope, dates, and operating conditions. The sources establish no current approved contract or deployment. [Scope](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#scope) [Evidence limits](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#evidence-limits)

## Accounting and reporting

Aspire uses a FileIT payment-accounting batch. EBBS describes real-time JSON accounting over Solace for listed entities. The Korea OLTP design describes accounting through KREDMI and FM Solace. [Selected accounting flows](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#payment-accounting-and-downstream-reporting)

The TLM query is limited to Korea entity `10036645`, records with status `SENT`, and a three-day maximum window. FMMIS, CIS, PacMan, MarketUDP/SSDR, and CNEDMp query RATAN cashflows through REST APIs. [TLM and query scope](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#payment-accounting-and-downstream-reporting)

## Cashflow and settlement processing

Murex describes MQ delivery for T−1 through T+1 and SFTP batches for T+2 through T+7. Corrective files use SFTP regardless of value date. The source excludes weekends and public holidays from batch delivery. [Murex cashflow windows](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing)

The Murex page requires RATAN batch ACK before the next batch. NACK requires Murex PSS investigation. A missing response for 30 minutes holds processing for Murex PSS investigation. FMSGW, Razor, and FXU describe separate settlement, feed, and utilization flows. [Murex response and related flows](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing)

SSI+ supplies SSI data through its API and sends record-change notifications over Solace. The candidate records distinct monitoring responsibilities for SSI+ PSS and RATAN PSS. [SSI+ flow and support](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing)

## Korea ENISIS transport remains unresolved

The Murex KR page describes SFTP for MX messages to ENISIS. The ENISIS page describes FM Solace for MX and MT210 messages. The selected pages do not explain the difference by message, stage, or design revision. [Both source descriptions](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#cashflow-and-settlement-processing) [Open question](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#open-questions)

The candidate preserves both routes and source-described recovery steps. It does not choose a current Korea transport. The proposed ENISIS exception blotter has no confirmed build or operating status.

## Related topics

- [[summaries/KT-settlement-korea-trade-confirmation|Korea COMP confirmation]] covers the separate payment confirmation gate.
- [[summaries/KT-settlement-lms-feed|LMS feed]] covers payment-feed eligibility and payload proposals.
- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back|Cashflow identity]] covers identity and status write-back questions.
- [[summaries/KT-settlement-auto-netting|Auto-netting]] covers netting rules and outcomes.

## Version 2 source-specific interface duties

The EBBS page places its real-time JSON objective within FMRP 2024 H1, without current rollout evidence.
Its literal code and country/location groups remain:

| Source code group | Source country/location text |
| --- | --- |
| `CN, MY, IN, SG` | `China, Malaysia, India, Singapore` |
| `UK, DE` | `United Kingdom, Germany` |
| `MU, AE, ID, PH, US, JP, ZA, HK, EG, NP, SA` | `MAURITIUS,DUBAI,JAKARTA,MANILA,NEWYORK,TOKYO,JOBURG,DIFC,PHILIP FCU, Hong Kong, Egypt, Nepal, Saudi` |

The last row has unequal code/name counts; it supplies no reliable position-based mapping.
ENISIS forwards received messages to the SWIFT network.
Its FM Solace route and MT210 conversion exception remain distinct from the Murex-KR SFTP description.
FMSGW classifies both MT and MX feeds as real-time Solace delivery; their country lists remain separate.
[Additional source-specific interface conditions](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#additional-source-specific-interface-conditions)

Murex sequence examples are `001,002,003…010`; payment count `ZZZZ` supports reconciliation.
The END file is required even without processed batches.
The previous summary's ACK-or-NACK next-batch wording is superseded by the source's ACK requirement.
NACK and the 30-minute timeout require investigation; automatic batch regeneration remains unavailable in this source description.
The separate UK candidate retains Ack/Nack wording and distinct recovery proposals.
These source scopes do not establish a shared approved replay contract.
[Catalog response condition](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#additional-source-specific-interface-conditions) [Separate UK candidate](../../../records/candidates/settlement/INT-KT-uk-murex-batch-contract.md#int-batch-01--uk-payment-bands-and-file-contract)

FXU sends accounting `FullUtilize` requests through Solace topics and queues; responses return from RATAN through Solace to FXU.
The source supplies no complete response schema or acknowledgement guarantee.
Razor describes `MX-FXCASH -> Ratan` for the BCS payment-status path.
Its source-specific exclusions, statuses, `SCBML V4.0`, and literal `2M` size limit remain distinct.
The size unit and a general direction for every catalog entry remain undefined.
[Source-specific FXU and Razor duties](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#additional-source-specific-interface-conditions)

SSI+ centrally maintains `Standard Settlement Instruction` data and exposes real-time queries through its ES cluster.
Updates, additions, and deletions trigger Solace notifications.
SSI+ PSS monitors API and notification availability, including agreed response time.
It informs RATAN PSS about planned downtime outside greenzone and unexpected outages.
RATAN PSS monitors subscriptions and contacts SSI+ PSS after a committed response-time breach.
These source-described duties establish no current contacts, service levels, or applicability.
[SSI ownership and support duties](../../../records/candidates/settlement/INT-KT-ratan-cashflow-settlement-interfaces.md#additional-source-specific-interface-conditions)
