---
type: KnowledgeTopic
id: KT-settlement-auto-netting-static-controls
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home
    Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting.md
  revision: sha256:a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62
  sha256: a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/page.md
  revision: sha256:a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62
  sha256: a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Cashflow Auto Netting.md
  revision: sha256:a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62
  sha256: a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:45:10.454315+08:00'
verified: []
scope: Historical selected-source design for settlement auto netting static controls.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which effective static rule/type mapping, Clearing_Swift_Suppress behavior, and
  net-over-net exceptions are approved?
- Which refresh/re-entry rule governs each operation and existing cashflow state?
- Which current roles, editable fields, default time, and STP bypass controls are
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
# Settlement auto netting static controls

## Scope

Historical selected-source design for settlement auto netting static controls.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Static rule access and validation

Only Data Ops may create or update auto-netting static; other users have read-only access.
A rule containing only booking entity is rejected.
An absent booking entity produces a warning that the rule applies to all booking locations.
Missing netting-ID exclusion also produces a warning.

Changing a rule netting type requires confirmation.

Sources: [original lines 34–36](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L34-L36), [original lines 54–56](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L54-L56).

### Netting-type conditions

CCIL type requires settlement method CCIL.
Missing counterparty exclusion for 400021949 produces a warning.
BIC type requires Counterparty_SCI_BIC_Net_Flag Y.
These validations differ: the counterparty exclusion is a warning, not a mandatory error.

The static UI also distinguishes manual and auto rule types.

Sources: [original lines 34–36](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L34-L36).

### Execution-key and resultant mappings

Bilateral grouping uses booking entity, counterparty, currency, and payment date.
CCIL grouping omits counterparty and maps resultant counterparty to 400021949, CLEARING CORP*MMB, with Cash settlement method.
BIC grouping adds SCI BIC-net flag and BIC code.
SAL MTM and SAL Coupon grouping add payment type.

Their resultant payment types retain the named netting type.

Sources: [original lines 34–34](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L34-L34).

### STP controls and inheritance

NSTP_MAKER_CHECKER requires maker and checker approval for the auto-netted exception.
NSTP_CHECKER_ONLY requires checker approval, plus maker handling when other exceptions require it.
FULL_STP remains disabled in the Day1 UI.
Its proposed bypass covers net-cashflow, pending-affirmation, and high-value exceptions, keeping the cashflow Unaffirmed.

Manual and auto resultants inherit DVP when any component is DVP, plus LIEN and commodity flags.
Intent-to-clear inheritance remains unresolved.

Sources: [original lines 34–34](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L34-L34), [original lines 63–66](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L63-L66).

### Rule refresh boundary and contradiction

The main requirement refreshes eligible unnetted WAITING/Pending Netting or Pending Exception and READY cashflows after rule creation.
Disabling refreshes tagged WAITING/Pending Auto Netting cashflows.
Updates include tagged pending-auto cashflows and eligible new matches.
The update text also lists Pending Auto Netting among exclusions, creating an ambiguity.

A historical no-refresh alternative remains in the clarification table.

Sources: [original lines 41–41](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L41-L41), [original lines 65–65](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L65-L65), [original lines 76–76](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L76-L76).

### Source-specific priority and result exceptions

The July review ranks SAL MTM, SAL Coupon, Clearing_Swift_Suppress, CCIL, BIC, and Bilateral types.
The main requirement resolves multiple matches by lowest priority number and later creation within a type.
It permits auto-netting over IRS resultants while otherwise prohibiting net-over-net.
The Clearing_Swift_Suppress resultant mapping and single-item treatment contain struck-through or differing source text.

Sources: [original lines 23–26](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L23-L26), [original lines 34–34](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L34-L34), [original lines 42–48](../../../evidence/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L42-L48).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which effective static rule/type mapping, Clearing_Swift_Suppress behavior, and net-over-net exceptions are approved?
- Which refresh/re-entry rule governs each operation and existing cashflow state?
- Which current roles, editable fields, default time, and STP bypass controls are approved?
