---
type: KnowledgeTopic
id: KT-settlement-korea-payment-routing
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2026 Changes/Cash Settlement -- Korea Migration/New Entity onboarding
    checking list - Korea 2026/page.md
  revision: sha256:84cf060ebee194f900f13aaab9d4176c9f6ff8c5007e6aa63ddc41e742b8700c
  sha256: 84cf060ebee194f900f13aaab9d4176c9f6ff8c5007e6aa63ddc41e742b8700c
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2026 Changes/Cash Settlement -- Korea Migration/RATAN to ENISIS/page.md
  revision: sha256:f742eae54e879b6928e98ef8fdaacff1589e107f583bde2cc8d6f67900bd357c
  sha256: f742eae54e879b6928e98ef8fdaacff1589e107f583bde2cc8d6f67900bd357c
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2026 Changes/Cash Settlement -- Korea Migration/Ratan to TIS/page.md
  revision: sha256:e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2
  sha256: e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2026 Changes/Cash Settlement -- Korea Migration/page.md
  revision: sha256:77d4c8db4af6922d53f80eb6999b1cb760f98024089ea7449d243a3e8979e26a
  sha256: 77d4c8db4af6922d53f80eb6999b1cb760f98024089ea7449d243a3e8979e26a
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2026 Changes/Korea Migration Functional Analysis/page.md
  revision: sha256:0c428d8027d9e4088a37306e6172ce47dd775208ac4229f74a42d1eb6e712c4a
  sha256: 0c428d8027d9e4088a37306e6172ce47dd775208ac4229f74a42d1eb6e712c4a
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:54:46.040257+08:00'
verified: []
scope: Historical selected-source design for settlement korea payment routing.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which Korea interface versions and routing filters are approved, including NOX versus
  NOS and acknowledgement-triggered states?
- Which validated rounding, currency, accounting, and language contracts complete
  Korea onboarding?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement korea payment routing

## Scope

Historical selected-source design for settlement korea payment routing.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Korea migration responsibilities

The target moves settlement processing from Murex Korea to RATAN.
RATAN sends SWIFT through ENISIS, posts real-time OLTP accounting, and uses SSI+ as instruction authority.
TLM supports suspense reconciliation.
Onboarding includes branch filters, currency cutoffs, SSI, rules, and entity-specific accounting setup.

The functional checklist explicitly prefers country-specific SSI before global-entity product-specific SSI.

Sources: [original lines 1–9](../../../evidence/sources/sha256/77d4c8db4af6922d53f80eb6999b1cb760f98024089ea7449d243a3e8979e26a.md#L1-L9), [original lines 11–31](../../../evidence/sources/sha256/77d4c8db4af6922d53f80eb6999b1cb760f98024089ea7449d243a3e8979e26a.md#L11-L31), [original lines 1–29](../../../evidence/sources/sha256/0c428d8027d9e4088a37306e6172ce47dd775208ac4229f74a42d1eb6e712c4a.md#L1-L29).

### ENISIS target transport and acknowledgements

The target replaces received MT conversion and SFTP with payment initiation and FM Solace transport.
MT210 remains an MT output; other specified output uses MX.
The selected condition requires RELEASED or SETTLED and NOS.
Tracking identity correlates acknowledgements.

FinalSentOK means acknowledgement, FinalCancelled means negative acknowledgement, and FirstSentOK means technical acknowledgement.
Onboarding adds FinalCancelled to the Swift Error default filter.

Sources: [original lines 1–5](../../../evidence/sources/sha256/f742eae54e879b6928e98ef8fdaacff1589e107f583bde2cc8d6f67900bd357c.md#L1-L5), [original lines 155–161](../../../evidence/sources/sha256/f742eae54e879b6928e98ef8fdaacff1589e107f583bde2cc8d6f67900bd357c.md#L155-L161), [original lines 237–242](../../../evidence/sources/sha256/f742eae54e879b6928e98ef8fdaacff1589e107f583bde2cc8d6f67900bd357c.md#L237-L242), [original lines 20–20](../../../evidence/sources/sha256/84cf060ebee194f900f13aaab9d4176c9f6ff8c5007e6aa63ddc41e742b8700c.md#L20-L20).

### TIS payment query boundary

The TIS filters select Korea entity10036645, requested settlement date, NOX, and Released or Settled nonreversal cashflows.
Pay-side accounts match UISUS or UIBOK; direct-debit receipts match UIDD.
Withdrawal and reversal flows remain outside query scope.
The manual payment categories must not generate RATAN SWIFT or accounting.

Post-release SSI updates are unsupported.
TIS query does not change RATAN status.
A beneficiary account dummy value is case-insensitive in the named BOK scenario.

Sources: [original lines 3–7](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L3-L7), [original lines 11–17](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L11-L17), [original lines 21–38](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L21-L38), [original lines 48–48](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L48-L48), [original lines 311–311](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L311-L311), [original lines 313–314](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L313-L314), [original lines 316–317](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L316-L317), [original lines 321–321](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L321-L321), [original lines 323–323](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L323-L323).

### TIS request and response scope

The request requires settDate in YYYY-MM-DD format.
The contract lists200,400,401,404, and500 outcomes.
Product group and type fields use expanded character lengths.
The source distinguishes KRO booking currency from KRW ISO currency.

External foreign-currency payments use ENISIS rather than the listed manual TIS categories.

Sources: [original lines 21–38](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L21-L38), [original lines 61–63](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L61-L63), [original lines 255–256](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L255-L256), [original lines 260–267](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L260-L267), [original lines 316–317](../../../evidence/sources/sha256/e130b012753d68321dc163b508307abccee4d8c276c980219388983ed6b463b2.md#L316-L317).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which Korea interface versions and routing filters are approved, including NOX versus NOS and acknowledgement-triggered states?
- Which validated rounding, currency, accounting, and language contracts complete Korea onboarding?
