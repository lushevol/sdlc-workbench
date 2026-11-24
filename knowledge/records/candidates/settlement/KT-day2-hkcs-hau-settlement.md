---
type: KnowledgeTopic
id: KT-day2-hkcs-hau-settlement
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-2d4d6a910d66ad89ebfb25d7
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/HKCS initiative/Onboarding for HAU currency/page.md
  revision: sha256:8272f1b9aaaac16467a7ed2a67b28900386968ddaf7e3e3e7f6cea33d9f3d045
  sha256: 8272f1b9aaaac16467a7ed2a67b28900386968ddaf7e3e3e7f6cea33d9f3d045
- id: SRC-0e52489bca29fdbd0d4c92f9
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/HKCS initiative/page.md
  revision: sha256:3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523
  sha256: 3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523
classification: settlement
scope: HKCS HAU settlement and SWIFT contract intent
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- KT-settlement-lms-feed
- INT-KT-payment-accounting-contracts
open_questions:
- 'KDQ-f4bc7e1b1d: Which effective HAU static values resolve the two Nostro/SWIFT
  BIC spellings, cutoff/calendar setup, DVP indicator, and MT605-versus-MT692 cancellation
  item?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:44:20.747525+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# HKCS HAU settlement and SWIFT contract intent

## Scope

HKCS HAU settlement and SWIFT contract intent.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### HKCS-01 — HAU settlement scope and lifecycle

The HKCS requirement covers FX booked in SCB HK, entity FMID 2, with gold represented as HAU.
The counter-currency cashflow is suppressed. HAU release cutoff is value date minus one business day at 10:00 GMT.
HAU uses the Hong Kong/HKD weekend and holiday calendar through non-ISO calendar mapping.
Approval limits follow XAU. The dated rounding answer specifies three decimals with rounding off.
RATAN sends no HAU settlement accounting; CIS queries RATAN. HAU messages still feed LMS.
The requirement specifies HAU MAIN Nostro and Vostro. Its Nostro-agent text differs from its SWIFT receiver spelling.
It gives `BKCHCHKHHGSI` for Nostro and `BKCHHKHHGSI` for SWIFT; this review does not silently normalize them.

[Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L1-L16). [Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L24-L37). [Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L49-L57).

### HKCS-02 — MT604 and MT605 generation

The proposed MT604/605 receiver is BKCHHKHHGSI. Field 23 is TRANSFER.
Field 26C needs the HAU-equivalent mapping. Its detailed mapping depends on an uninspected image.
Field 32F uses FOZ and commodity quantity, with at most three decimals.
Field 87A identifies the receiving DP for MT604 and paying DP for MT605.
For MT604 field 88A without an account, use the beneficiary BIC from entity-sender static.
With an account, use slash plus account on line 1 and beneficiary BIC on line 2.
MT605 uses entity sender BIC. The table also retains a field 88D branch labelled not expected in BAU.
That conditional branch must not become a universal permission to omit beneficiary data.

[Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L24-L25).

### HKCS-03 — SCT and DVP instructions

Non-PVP SCT uses `/ACC/SCRTRF`; SSI continuation lines start with `//`.
For DVP, field 72 starts `/ACC/DVPTRF`, followed by `/OCMT/` plus ISO currency, formatted amount, and slash.
The other-leg lookup uses trade ID and value date for Murex, adding major version for Stella.
The permitted settlement currencies are HKD, USD, EUR, and CNY. Non-ISO counter currencies require ISO mapping.
The amount supports at most 13 integer digits and two decimals, with comma decimal separator and no thousands separator.
Missing or multiple other-leg matches leave READY with a SWIFT generation error. Missing mandatory fields have the same outcome.
The source specifies reinstate/regeneration handling. Unexpected blockage escalates to CTMU.
Murex strategy PVP and Stella settlement method PVP are listed as indicators. A separate clarification uses the DVP NSTP rule.
Their precise equivalence remains unresolved.

[Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L24-L25). [Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L27-L30). [Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L57).

### HKCS-04 — Cancellation and source-version limits

MT692 field 20 uses `CANC` plus cashflow ID. Field 11S uses the original new message last-update time.
It does not use the withdrawal event date.
The history adds this requirement on 30 September 2026. Linked sample SWIFT and confirmation attachments were not inspected.

[Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L1-L11). [Original evidence](../../../evidence/sources/sha256/3b343203fb430bd95b7f86b1c590dd2988e29fb0278bb7940f282f713b03f523.md#L26).

### HKCS-05 — Onboarding dependencies and unresolved cancellation item

The onboarding design requires HAU currency dropdown support, three-decimal rounding, precious-metal SWIFT static, and no HAU accounting publication.
It also requires LMS publication and a missing-Vostro exception for HAU receipts.
Cutoff configuration initially says to copy XAU. The later dated business requirement explicitly uses HKD calendar mapping and the HAU cutoff.
The onboarding TBD list says MT605 field 20 should use CANC. The later business requirement instead specifies MT692.
Their cancellation-message scope requires confirmation. Source labels of no change do not establish deployed configuration.

[Original evidence](../../../evidence/sources/sha256/8272f1b9aaaac16467a7ed2a67b28900386968ddaf7e3e3e7f6cea33d9f3d045.md#L5-L18). [Original evidence](../../../evidence/sources/sha256/8272f1b9aaaac16467a7ed2a67b28900386968ddaf7e3e3e7f6cea33d9f3d045.md#L20-L25).

## Connections

Related canonical IDs: `KT-settlement-lms-feed`, `INT-KT-payment-accounting-contracts`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
