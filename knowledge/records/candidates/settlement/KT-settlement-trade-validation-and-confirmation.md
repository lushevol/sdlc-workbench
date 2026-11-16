---
type: KnowledgeTopic
id: KT-settlement-trade-validation-and-confirmation
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Trade Confirmation & Cashflow STP/page.md
  revision: sha256:fc741b7ca9888a2210e6d48f581b2ec703a980ad23b3e56cf2045c03e22d1387
  sha256: fc741b7ca9888a2210e6d48f581b2ec703a980ad23b3e56cf2045c03e22d1387
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Trade Validation & Cashflow Process/RATAN Settlement Control on Trade
    Validation/page.md
  revision: sha256:7d46cefe59c45a24ed821599d37f99bf9f31e618f90dcb5bac57904f76c6b871
  sha256: 7d46cefe59c45a24ed821599d37f99bf9f31e618f90dcb5bac57904f76c6b871
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Trade Validation & Cashflow Process/UAT test cases - Murex 2.11 booking/page.md
  revision: sha256:182c9188dd1fe97dbf895f6b374b62d603ea041b282db8e3a8613ac48da8c092
  sha256: 182c9188dd1fe97dbf895f6b374b62d603ea041b282db8e3a8613ac48da8c092
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Trade Validation & Cashflow Process/page.md
  revision: sha256:2c16953d76b71f833ecbaf0e6a9fe00bfaf1bc8a740839828c1f6049e5728098
  sha256: 2c16953d76b71f833ecbaf0e6a9fe00bfaf1bc8a740839828c1f6049e5728098
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/MX2.11 Decomm
    - Cash Settlement Business Workflow/Affirmation   Confirmation Status driving
    Settlement STP/page.md
  revision: sha256:5392f75dcfd2ed47a91abd30a1c05e054d01c8a8406dc8e096ea2fa0461463d3
  sha256: 5392f75dcfd2ed47a91abd30a1c05e054d01c8a8406dc8e096ea2fa0461463d3
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:50:56.332213+08:00'
verified: []
scope: Historical selected-source design for settlement trade validation and confirmation.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which effective validation and confirmation state matrices and bypass scopes are
  approved?
- What prevents release of version1 while version2 remains in the Group Blotter?
- Which special-product STP decisions and legal or reconciliation prerequisites are
  approved?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement trade validation and confirmation

## Scope

Historical selected-source design for settlement trade validation and confirmation.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Validation gates visibility

The target holds unvalidated cashflows outside the settlement GUI.
Trade validation resumes matching cashflows in the main settlement workflow.
Stella correlation uses trade ID and trade major version.
Murex correlation uses source-system trade internal ID against cashflow Trade_Id.

The examples distinguish validation of a new trade from validation of its later cancellation.

Sources: [original lines 1–12](../../../evidence/sources/sha256/2c16953d76b71f833ecbaf0e6a9fe00bfaf1bc8a740839828c1f6049e5728098.md#L1-L12), [original lines 15–51](../../../evidence/sources/sha256/2c16953d76b71f833ecbaf0e6a9fe00bfaf1bc8a740839828c1f6049e5728098.md#L15-L51), [original lines 53–57](../../../evidence/sources/sha256/2c16953d76b71f833ecbaf0e6a9fe00bfaf1bc8a740839828c1f6049e5728098.md#L53-L57).

### Source-specific accepted validation states

Cashflow-level Murex validation accepts VALD or CONFIRMED.
Other cashflow sources accept SENT, ECONAFFIRMED, AFFIRMED, ECONCONFIRMED, CONFIRMED, or NONCONFIRMED.
Stella parent validation additionally permits TOBESENT with action Validate.
Murex parent validation accepts VALD or COMP.

These source-specific state vocabularies must remain distinct.

Sources: [original lines 15–51](../../../evidence/sources/sha256/2c16953d76b71f833ecbaf0e6a9fe00bfaf1bc8a740839828c1f6049e5728098.md#L15-L51).

### Validation bypass and migration conditions

The Stella bypass covers the named Egypt, Nepal, and Saudi entities, SCF, and LoanDeposit.
It also covers enumerated China entities for Spot, Forward, NDF, and Swap.
The source contains exact FMID and taxonomy predicates.
The dated migration plan retains China BAU and manual exception handling.

Its planned SCF/LoanDepo auto-validation milestone is explicitly tentative.

Sources: [original lines 15–51](../../../evidence/sources/sha256/2c16953d76b71f833ecbaf0e6a9fe00bfaf1bc8a740839828c1f6049e5728098.md#L15-L51), [original lines 8–10](../../../evidence/sources/sha256/7d46cefe59c45a24ed821599d37f99bf9f31e618f90dcb5bac57904f76c6b871.md#L8-L10).

### Confirmation exception handling

Stella AFFIRMED, CONFIRMED, or NONCONFIRMED can close Pending Confirmation/Affirmation.
Murex COMP can close that exception for matching trade cashflows.
Removing the only exception permits STP.
Cancellation withdrawal is a special STP case bypassing settlement exception checks.

The source filters trade-expiry cashflows.

Sources: [original lines 1–19](../../../evidence/sources/sha256/fc741b7ca9888a2210e6d48f581b2ec703a980ad23b3e56cf2045c03e22d1387.md#L1-L19), [original lines 22–24](../../../evidence/sources/sha256/fc741b7ca9888a2210e6d48f581b2ec703a980ad23b3e56cf2045c03e22d1387.md#L22-L24).

### Product-specific affirmation proposal

The decommission proposal separates trade affirmation, confirmation matching, and manual cashflow affirmation.
Gross trade cashflows generally permit full affirmation, full matching, or cashflow affirmation.
FX swap legs follow their own product and tenor.
Fixing cashflows require full trade matching plus completed fixing.

Its table explicitly rejects full affirmation plus fixing as sufficient.
Internal, inter-entity, negative-affirmation, netting, clearing, and Islamic cases retain separate conditions or unresolved decisions.

Sources: [original lines 1–18](../../../evidence/sources/sha256/5392f75dcfd2ed47a91abd30a1c05e054d01c8a8406dc8e096ea2fa0461463d3.md#L1-L18).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which effective validation and confirmation state matrices and bypass scopes are approved?
- What prevents release of version1 while version2 remains in the Group Blotter?
- Which special-product STP decisions and legal or reconciliation prerequisites are approved?
