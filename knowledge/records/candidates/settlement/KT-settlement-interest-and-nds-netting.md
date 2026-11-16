---
type: KnowledgeTopic
id: KT-settlement-interest-and-nds-netting
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-5dee32f05ce117b49aec32d7
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home
    Page/Functional Requirement/Netting/IRS Fix Leg & Floating leg payment handling.md
  revision: sha256:4041381744e47a709d66526f630e08673e48cfe6657592ba1a7e7b302db120cd
  sha256: 4041381744e47a709d66526f630e08673e48cfe6657592ba1a7e7b302db120cd
- id: SRC-9241449744a79d41134acf6c
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/IRS Fix Leg & Floating leg payment handling.md
  revision: sha256:4041381744e47a709d66526f630e08673e48cfe6657592ba1a7e7b302db120cd
  sha256: 4041381744e47a709d66526f630e08673e48cfe6657592ba1a7e7b302db120cd
- id: SRC-7cdd706104b50bf966b5d71e
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/IRS Fix Leg & Floating leg payment handling/page.md
  revision: sha256:f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d
  sha256: f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d
- id: SRC-4e9732528edbf3bc8a80dc89
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home
    Page/Functional Requirement/Netting/NDS Auto Netting.md
  revision: sha256:1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d
  sha256: 1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d
- id: SRC-fb926c5c667e80bbfae2d99f
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/NDS Auto Netting/page.md
  revision: sha256:1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d
  sha256: 1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d
- id: SRC-b92254f37d821df4383ad248
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/NDS Auto Netting.md
  revision: sha256:1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d
  sha256: 1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d
classification: settlement
scope: IRS leg completeness and NDS netting proposal
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- KT-settlement-auto-netting
- KT-settlement-manual-netting
- KT-settlement-amendment-reversal-rebook-exceptions
open_questions:
- 'KDQ-9511672705: Which IRS source variant is authoritative for each scope?'
- 'KDQ-036248d4f1: Should an IRS auto-net resultant be WAITING or VERIFIED, and which
  checks permit that state?'
- 'KDQ-49cf85ee9f: Does expected count use cashflow ID/value date or schedule date/currency?'
- 'KDQ-8cfadd6df9: Which file ordering, retry, and late-arrival policies govern fixing
  flags?'
- 'KDQ-6770c55ad3: Which calendar and time zone define the NDS three-business-date
  scan?'
- 'KDQ-c56789eff6: What wait, retry, or exception rule applies when TDS3 parent typology
  is absent?'
- 'KDQ-fecd0eeee9: Which NDS Payment_Type row takes precedence: blank or NDS Fixing
  Netting?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:57:22.308587+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# IRS leg completeness and NDS netting proposal

## Scope

IRS leg completeness and NDS netting proposal.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### L3-IRS-01 — Regional Murex fixing gates

For CN, SG, IN, and MY, the real-time VD-7 fixed leg with pending-fixing Y waits for another leg. Murex sends reversal and net amount after fixing; cancel the fixed leg and process the net cashflow. UK/DE batch VD-2 through VD-7 has the same Y hold. Real-time reversal/net replacements with X create Fixing Unknown; the correcting file supplies N. Process file corrections only for WAITING, Pending Exception, Pending Operator or Pending Verification, and Fixing Unknown. Do not reprocess an already-cancelled reversal. Batch N continues normal checking.

[Original evidence](../../../evidence/sources/sha256/4041381744e47a709d66526f630e08673e48cfe6657592ba1a7e7b302db120cd.md#L1-L103). [Original evidence](../../../evidence/sources/sha256/4041381744e47a709d66526f630e08673e48cfe6657592ba1a7e7b302db120cd.md#L111-L189).

### L3-IRS-02 — UK/DE near-date and source-specific leg count

For UK/DE real-time VD through VD-1, X blocks as Fixing Unknown. Correcting file Y moves to Pending Another Leg; N continues checks. Stella IRS-interest detection covers FixedFloat, OIS, FloatFloat, and FixedFixed with Coupon/Fixed or Coupon/Float, excluding Withdrawals. Compare RATAN and TDX counts for the same cashflow ID and value date; fewer RATAN cashflows waits for another leg. The Murex branch uses pending-fixing Y and excludes Withdrawals.

[Original evidence](../../../evidence/sources/sha256/f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d.md#L1-L103). [Original evidence](../../../evidence/sources/sha256/f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d.md#L111-L179).

### L3-IRS-03 — Aggregation and scenario limits

The parent view proposes within-trade fixed/floating auto-netting and cross-trade aggregation. Refixing before release auto-un-nets and re-nets. Intermediate resultants die and components link to the final resultant. Some example arithmetic is inconsistent, including a fixed amount changing from 100 to 200 with a displayed 120 resultant. These are expected scenarios, without actual failure or test-pass evidence. Do not derive corrected accounting values from inconsistent examples.

[Original evidence](../../../evidence/sources/sha256/4041381744e47a709d66526f630e08673e48cfe6657592ba1a7e7b302db120cd.md#L1-L103). [Original evidence](../../../evidence/sources/sha256/4041381744e47a709d66526f630e08673e48cfe6657592ba1a7e7b302db120cd.md#L111-L189).

### L3-IRS-04 — Distinct resultant states and release boundaries

The child within-trade example uses VERIFIED where the parent uses WAITING. No source establishes precedence. The settled-refixing example holds withdrawal and replacement in WAITING with Cancel / Amend after payment release, followed by manual netting. This does not replace NDS REVERSAL/REBOOK semantics. Manual netting with two CDS trades and a pending IRS fixed leg is a specific request, without a universal bypass. The final un-net section is explicitly NOT Required for Day 1.

[Original evidence](../../../evidence/sources/sha256/f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d.md#L1-L103). [Original evidence](../../../evidence/sources/sha256/f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d.md#L111-L179).

### L3-IRS-05 — FMRP unequal schedule exception

The different-value-date proposal applies only to FMRP, excluding Murex 2.11. Query TDSX by trade ID and inspect first- and second-leg periodicAdjustedInterestPaymentDate lists. A schedule with only one leg bypasses Pending Another Leg and continues checks. The wording about a date absent from either leg remains ambiguous. Serialized trade fixtures and images do not fill that gap.

[Original evidence](../../../evidence/sources/sha256/f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d.md#L1-L103). [Original evidence](../../../evidence/sources/sha256/f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d.md#L111-L179).

### L3-NDS-01 — NDS scope and scheduler

RATAN must net NDS by NID while Murex stops NDS netting. Product scope names NDS, NDS Fixing, NDIRS, NDCF, NDFRA, ND CDS Fixing, ND CDS, and ND-Convert. Group by booking entity, counterparty, value date, currency, and NID. Scan every 30 minutes for today through two business days ahead, WAITING with Pending Exception containing Pending NDS Netting. That NSTP rule must be live. Group Blotter must permit normal progression into eligibility.

[Original evidence](../../../evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md#L1-L21). [Original evidence](../../../evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md#L24-L68).

### L3-NDS-02 — NDIRS exception and parent dependency

NDIRS USD fixing settles in deliverable currency and is STP without this netting. Other scoped components, including ND CCS, are NSTP. Confirmation match must follow the Murex logic, whose full contract is not reproduced. Query parent typology from TDS3 using the NID-linked parent trade; take the final pipe-delimited source-instrument-type value. Arrival order can leave that value empty; handling remains unresolved.

[Original evidence](../../../evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md#L1-L21). [Original evidence](../../../evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md#L24-L68).

### L3-NDS-03 — NDS amendment and resultant rules

Before release, amendment or refixing auto-un-nets and re-nets reversal/new next cycle. Cancellation cancels the original and leaves the remaining component waiting if no partner arrives. After release, reversal/new require NSTP REVERSAL and REBOOK manual handling. System and manual un-net are prohibited after payment release. Before release, manually netting the resultant with other products is proposed. The resultant uses N plus 11 digits, UUID message/netting IDs, QUEUED, Unaffirmed, GROSS, CASH, TOBESENT, and zero versions. Common family/group/type/typology/strategy/trade/taxonomy values inherit only when equal, else blank. CFI comes from the non-NDS-Fixing component; other attributes use the first component. Payment_Type appears both blank and NDS Fixing Netting; ordering and precedence remain unresolved.

[Original evidence](../../../evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md#L1-L21). [Original evidence](../../../evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md#L24-L68).

## Connections

Related canonical IDs: `KT-settlement-auto-netting`, `KT-settlement-manual-netting`, `KT-settlement-amendment-reversal-rebook-exceptions`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
