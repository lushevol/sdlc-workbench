---
type: KnowledgeTopic
id: KT-settlement-clearing-and-swap-agent-boundaries
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2024 changes/Q3 Function Analysis/Clearing Trades & Payment Risk/page.md
  revision: sha256:ae8c762fb93203dc70026807b0c52acad3b5c71e11aa0ffaaf4b2d7b6597bd67
  sha256: ae8c762fb93203dc70026807b0c52acad3b5c71e11aa0ffaaf4b2d7b6597bd67
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2024 changes/Q3 Function Analysis/Swap Agent Payment/page.md
  revision: sha256:0c6d461490909360ae049eb7253577a04d4cb7dfadb6dbb53328a9dc8b17cc2f
  sha256: 0c6d461490909360ae049eb7253577a04d4cb7dfadb6dbb53328a9dc8b17cc2f
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2024 changes/RFR and Swap Agent/page.md
  revision: sha256:f3be0790afd5855899399d5e3edcd0c1c08cd9e4732750f2d32528427cc6a7df
  sha256: f3be0790afd5855899399d5e3edcd0c1c08cd9e4732750f2d32528427cc6a7df
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:54:45.962877+08:00'
verified: []
scope: Historical selected-source design for settlement clearing and swap agent boundaries.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which clearing indicator or alternative NSTP rule is approved and validated against
  nonclearing trades?
- Which Swap Agent principal, netting, and dummy-identity contracts supersede the
  earlier proposal?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement clearing and swap agent boundaries

## Scope

Historical selected-source design for settlement clearing and swap agent boundaries.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Clearing payment safety objective

The ideal booking model identifies intended clearing before novation.
Original bilateral payments must not STP while awaiting clearing novation.
Post-novation clearing payments require accounting without bilateral settlement.
The source proposes trade-level clearing indicators or a source-system NSTP rule.

The latter requires evidence that legitimate nonclearing trades will not be stopped.

Sources: [original lines 3–8](../../../evidence/sources/sha256/ae8c762fb93203dc70026807b0c52acad3b5c71e11aa0ffaaf4b2d7b6597bd67.md#L3-L8), [original lines 34–36](../../../evidence/sources/sha256/ae8c762fb93203dc70026807b0c52acad3b5c71e11aa0ffaaf4b2d7b6597bd67.md#L34-L36), [original lines 38–41](../../../evidence/sources/sha256/ae8c762fb93203dc70026807b0c52acad3b5c71e11aa0ffaaf4b2d7b6597bd67.md#L38-L41).

### Swap Agent payment split

The earlier Swap Agent proposal settles initial and final principal bilaterally.
Interim coupon and principal require accounting without bilateral payment.
All payments use Main Nostro accounting.
Its no-netting statement differs from the later manual-netting requirement.

The source also contains inconsistent trade numbering in its proposed SSI assignment.

Sources: [original lines 1–12](../../../evidence/sources/sha256/0c6d461490909360ae049eb7253577a04d4cb7dfadb6dbb53328a9dc8b17cc2f.md#L1-L12), [original lines 18–36](../../../evidence/sources/sha256/0c6d461490909360ae049eb7253577a04d4cb7dfadb6dbb53328a9dc8b17cc2f.md#L18-L36), [original lines 5–5](../../../evidence/sources/sha256/f3be0790afd5855899399d5e3edcd0c1c08cd9e4732750f2d32528427cc6a7df.md#L5-L5).

### Dated payment mapping and accounting narrative

The January2025 mapping distinguishes Initial Notional, Interim MTM, Coupon, and Final Notional using strategy, typology, and flow indicators.
SWAP_AGENT cashflows require NSTP.
Interim MTM and Coupon without a netting ID require netting.
Accounting narrative joins strategy, payment type, and netting ID with hash separators.

Missing values remain empty and the result truncates to65 characters.

Sources: [original lines 94–108](../../../evidence/sources/sha256/f3be0790afd5855899399d5e3edcd0c1c08cd9e4732750f2d32528427cc6a7df.md#L94-L108), [original lines 110–117](../../../evidence/sources/sha256/f3be0790afd5855899399d5e3edcd0c1c08cd9e4732750f2d32528427cc6a7df.md#L110-L117).

### Exceptional empty-flow proposal

The proposed exception applies to RECALC or SWAP_AGENT, trade reference0, and blank typology.
It enriches missing flows and validation state before processing.
The text describes R-prefixed flow-based trade IDs, while tables also show MTR-prefixed original IDs.
Dummy identity removal before downstream feeds remains an unresolved design choice.

Sources: [original lines 120–134](../../../evidence/sources/sha256/f3be0790afd5855899399d5e3edcd0c1c08cd9e4732750f2d32528427cc6a7df.md#L120-L134).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which clearing indicator or alternative NSTP rule is approved and validated against nonclearing trades?
- Which Swap Agent principal, netting, and dummy-identity contracts supersede the earlier proposal?
