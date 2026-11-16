---
type: Summary
description: "Keeps settlement feed status, timing, retries, storage, and destination-specific accounting variants distinct."
doc_type: short
full_text: sources/KT-settlement-feeds-p3.md
---

> **Candidate/draft only:** The feed variants do not establish an approved or deployed contract. Owner is unknown; `verified` is empty.

# Settlement feeds p3

The selected designs distinguish Razor status write-back from publication payloads: ACK/NACK, RELEASED, and SETTLED have different meanings, while the adaptor examples batch netted component IDs and use a single ID for gross cashflows. LMS and trade feeds carry separate source-stack, entity, and identity proposals. These descriptions do not define one shared payload.

EBBS uses event-driven publication, value-date handling, and bounded retries for listed error codes. Aspire describes batch publication from 22:05 local time on value date. The after-midnight date rule and storage-column choice remain unresolved. Korea accounting sources also differ: EBBS and OLTP use separate messages, bridge-account rules, acknowledgement topics, and retry behavior. The OLTP source specifies no retry for its Korean tasks. A Swift fragment retains an existing connection but adds no new wire contract.

The [[summaries/KT-settlement-lms-feed]] and [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]] pages preserve related candidate scope and route questions. This source set supplies no current approval, consumer confirmation, or execution evidence.

## Canonical sections

- [Status write-back contract](../../../records/candidates/settlement/KT-settlement-feeds-p3.md#status-write-back-contract)
- [EBBS and Aspire publication variants](../../../records/candidates/settlement/KT-settlement-feeds-p3.md#ebbs-and-aspire-publication-variants)
- [Korea accounting task differences](../../../records/candidates/settlement/KT-settlement-feeds-p3.md#korea-accounting-task-differences)
- [Reversal and reinstatement limits](../../../records/candidates/settlement/KT-settlement-feeds-p3.md#reversal-and-reinstatement-limits)

## Source-specific downstream and task predicates

The write-back fragment names STELLA or Murex2.11. It does not establish the same contract for other Murex versions. [Canonical detail](../../../records/candidates/settlement/KT-settlement-feeds-p3.md#historical-write-back-downstream-version)

The LMS proposal maps default Murex/Stella MessageSender FMRP to Stack Flow FMRPSTELLA. LoanIQ maps LOANIQ to FMRPSTELLA-LOANIQ. LMS alignment is required; the source supplies no compatibility execution evidence. [Canonical detail](../../../records/candidates/settlement/KT-settlement-feeds-p3.md#proposed-lms-identifier-migration)

Korean EBBS uses one bridge account per entity; OLTP chooses by currency. Its SOD job selects Hold tasks with payment_date at most current_date. Missing Request_info or ExtColumn2 JSON is generated before processing. Additional OLTP BIC mapping remains unspecified. [Canonical detail](../../../records/candidates/settlement/KT-settlement-feeds-p3.md#korean-accounting-selection-and-validation-conditions)

Reinstate after FAILED produces tag reinstate; approval after SWIFT_SUPPRESSED produces SwiftUnSuppressed. The stated filter combines reinstate with last published balance below zero. Other reversal and idempotency decisions remain unresolved. [Canonical detail](../../../records/candidates/settlement/KT-settlement-feeds-p3.md#reinstatement-trigger-and-reversal-tags)
