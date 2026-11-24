---
type: KnowledgeTopic
id: KT-day2-auto-dvp
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Auto DVP (eBBS)/AutoDVP UAT testing/page.md
  revision: sha256:113260f60f491e94f10fd5e51d390f965bde3a5a22c3e4d3435c9d1c4a44893c
  sha256: 113260f60f491e94f10fd5e51d390f965bde3a5a22c3e4d3435c9d1c4a44893c
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Auto DVP (eBBS)/page.md
  revision: sha256:0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22
  sha256: 0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:43:26.309055+08:00'
verified: []
scope: Historical selected-source design for day2 auto dvp.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which country/entity scope applies, and is eligibility based on booking entity or
  the account country in RTA?
- Which calendar, payment-date rule, reference extraction, and amendment identity
  govern matching?
- What happens after a settled pair is amended, including major-version change and
  netted difference payments?
- What stores prior receipt evidence, deduplicates notifications, and permits replay
  after consumption failure?
- Which owner and effective source approve AutoDVP rules, and where are the UAT execution
  artifacts?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Day2 auto dvp

## Scope

Historical selected-source design for day2 auto dvp.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### EBBS receipt notification boundary

The AutoDVP requirement initially covers EBBS notifications for external counterparties with accounts held at SCB.
It consumes CorporateFinancial RTA with CreditDebitFlag D.
InternalAccount-only notifications remain outside scope.
The pilot heading proposes six countries, while scenarios refer to seven.

The country/entity scope therefore remains unresolved.

Sources: [original lines 30–40](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L30-L40), [original lines 117–166](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L117-L166), [original lines 225–230](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L225-L230).

### Source-specific CCS product predicates

The source covers Murex and Stella CCS.
Murex uses Instrument_Common__ISDA_Taxonomy IRD|CS.
Stella uses InterestRate:CrossCurrency taxonomy suffixes FixedFloat, Basis, FixedFixed, and FloatFloat.
New products require configuration changes under this design.

Sources: [original lines 168–183](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L168-L183).

### Receive verification and pay linkage

RTA currency and amount must equal the RATAN receive cashflow values.
RTA value date must fall from payment date through payment date plus two business days, inclusive.
The June 26 linkage uses trade ID, payment date, and the first six payment-type characters.
For Murex, a null payment type is omitted from the query.

Stella additionally requires major version.

Sources: [original lines 185–203](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L185-L203).

### Recognized DVP exceptions and closure

Only exception codes DVP Strategy and DVP count as DVP exceptions for this flow.
A different user-created code, such as DVP AAA, does not qualify.
After qualifying receipt evidence, only a WAITING pay cashflow with a recognized DVP exception qualifies for automatic closure.
Other pay states remain unchanged.

The requirement requests a green DVP Received tag in pay-cashflow details.

Sources: [original lines 24–28](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L24-L28), [original lines 214–223](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L214-L223).

### Resultants and split cashflows

RTA for a received netting resultant or split child does not trigger this AutoDVP flow.
A linked pay cashflow whose ID starts with N is skipped.
One received parent may close DVP exceptions on its split pay children that remain WAITING.
Multiple independent pay cashflows require manual handling.

The ND CCS pay-resultant case remains outside scope.

Sources: [original lines 21–28](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L21-L28), [original lines 237–238](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L237-L238).

### Withdrawal and amended linkage limits

The flow ignores receipt withdrawal events.
The stated withdrawal scenarios retain pay-side DVP exceptions.
For an amended cashflow with unchanged linkage, the replacement can receive automatic DVP closure.
When trade identity changes, the stated scenarios retain the exception.

These cases do not authorize linking by original trade ID without a further decision.

Sources: [original lines 23–23](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L23-L23), [original lines 239–244](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L239-L244).

### Arrival order and operator fallback

The requirement scenario expects receipt evidence before pay arrival to prevent a later pay DVP exception.
Consumption failure requires manual handling when automatic closure cannot occur.
The selected source does not define retention, deduplication, or replay guarantees for that evidence.

Sources: [original lines 28–28](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L28-L28), [original lines 234–234](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L234-L234).

### Future scope remains separate

More countries and products are future extensions.
External-bank accounts, cross-border debit, and MT910 are listed as future considerations.
These entries do not extend the initial EBBS boundary.

Sources: [original lines 279–286](../../../evidence/sources/sha256/0d1e3b39d40792da18aace1cbc926cf51823926d99fbebf0f5693b76f7e89b22.md#L279-L286).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which country/entity scope applies, and is eligibility based on booking entity or the account country in RTA?
- Which calendar, payment-date rule, reference extraction, and amendment identity govern matching?
- What happens after a settled pair is amended, including major-version change and netted difference payments?
- What stores prior receipt evidence, deduplicates notifications, and permits replay after consumption failure?
- Which owner and effective source approve AutoDVP rules, and where are the UAT execution artifacts?
