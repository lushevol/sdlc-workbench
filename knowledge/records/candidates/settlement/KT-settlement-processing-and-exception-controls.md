---
type: KnowledgeTopic
id: KT-settlement-processing-and-exception-controls
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/MX2.11 Decomm
    - Cash Settlement Business Workflow/NSTP Workflow/page.md
  revision: sha256:a7a08f1eb91a47107c93985da662ca9cfb6bd3bd6d6891e3177be7b3fec5a65d
  sha256: a7a08f1eb91a47107c93985da662ca9cfb6bd3bd6d6891e3177be7b3fec5a65d
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/MX2.11 Decomm
    - Cash Settlement Business Workflow/RATAN Cashflow Status - CHINA and beyond/page.md
  revision: sha256:7f3e2a5d118de2e0678431263bb9f4391aa4df0011ac58c3e78d01b520c12d82
  sha256: 7f3e2a5d118de2e0678431263bb9f4391aa4df0011ac58c3e78d01b520c12d82
- resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  1_Precheck/page.md
  revision: sha256:8b38524860635e161456b4240c06f2273561413b75436803043901c08a1d8ae9
  sha256: 8b38524860635e161456b4240c06f2273561413b75436803043901c08a1d8ae9
- resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  2_Suppression
    Rule Check/page.md
  revision: sha256:aa26d8534029330abaf84b48a3a4fe84418776af4798ab15fe716baa8b72f026
  sha256: aa26d8534029330abaf84b48a3a4fe84418776af4798ab15fe716baa8b72f026
- resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  3_Cashflow
    Stamp/page.md
  revision: sha256:62c7b1cbb5b7240618cdc110113e69cd8c3d26e6a0c3bcea5682de3fa1b9f2e0
  sha256: 62c7b1cbb5b7240618cdc110113e69cd8c3d26e6a0c3bcea5682de3fa1b9f2e0
- resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  5.0_SSI
    Stamping/page.md
  revision: sha256:98270609f797c85a3c3e3f482c08c82f8bac86a0ec8fca22a27358f4f6fd7507
  sha256: 98270609f797c85a3c3e3f482c08c82f8bac86a0ec8fca22a27358f4f6fd7507
- resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  5.1_Multi
    Exception Rule Check/page.md
  revision: sha256:bb673d577aa8824afc835778505b0e2970f55e645a52e1ce35585d75b97d6e5c
  sha256: bb673d577aa8824afc835778505b0e2970f55e645a52e1ce35585d75b97d6e5c
- resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  6_SWIFT/page.md
  revision: sha256:97226b3c39ebbcb4be4ac414c156ad2b656ad04bc0629dd2cc9ec3352d5efae9
  sha256: 97226b3c39ebbcb4be4ac414c156ad2b656ad04bc0629dd2cc9ec3352d5efae9
- resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  7_Last
    Mile Check/page.md
  revision: sha256:e088ccc338da682e1e0640a1c685a43444a85c1fbf36ecf9e7cec4d248e26c70
  sha256: e088ccc338da682e1e0640a1c685a43444a85c1fbf36ecf9e7cec4d248e26c70
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:52:25.882351+08:00'
verified: []
scope: Historical selected-source design for settlement processing and exception controls.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which exception matrix, authority limits, and Day1/Day2 controls govern current
  operation?
- What exact last-mile economic uniqueness and override contract is approved?
- Which expected-count and SSI selection scopes are approved?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement processing and exception controls

## Scope

Historical selected-source design for settlement processing and exception controls.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Maker-checker exception handling

The NSTP design uses exception-specific maker, checker, authority-limit, and automatic-resolution rules.
Rejected SSI input preserves the maker values.
Repeated blind verification covers mismatched or newly enriched fields.
Ad-hoc SSI retains maker input despite later upstream refresh.

Previously netted cashflows require an approver distinct from the unnetting user.
High-value manual-touch handling applies above USD100 million in this historical table.

Sources: [original lines 1–87](../../../evidence/sources/sha256/a7a08f1eb91a47107c93985da662ca9cfb6bd3bd6d6891e3177be7b3fec5a65d.md#L1-L87), [original lines 13–13](../../../evidence/sources/sha256/bb673d577aa8824afc835778505b0e2970f55e645a52e1ce35585d75b97d6e5c.md#L13-L13).

### Suppression and failure boundaries

Cashflow suppression removes both payment and accounting.
Payment or SWIFT suppression retains accounting.
Manual suppression uses maker/checker.
Unsuppression is permitted only until value date in the historical workflow.

Released or settled cashflows cannot be manually failed.
Failed reinstatement requires maker/checker payment-date selection.
Post-release failures require the named external handling route.

Sources: [original lines 1–87](../../../evidence/sources/sha256/a7a08f1eb91a47107c93985da662ca9cfb6bd3bd6d6891e3177be7b3fec5a65d.md#L1-L87), [original lines 9–14](../../../evidence/sources/sha256/aa26d8534029330abaf84b48a3a4fe84418776af4798ab15fe716baa8b72f026.md#L9-L14), [original lines 20–20](../../../evidence/sources/sha256/aa26d8534029330abaf84b48a3a4fe84418776af4798ab15fe716baa8b72f026.md#L20-L20).

### China status and acknowledgement model

The China table distinguishes projected, queued, waiting, ready, released, settled, netted, split, and terminal states.
FMSRE acknowledgement establishes Released.
AMH or SCPAY acknowledgement establishes Settled in its payment model.
Released, Settled, Netted, and Split are sent to Stella.

The table marks Nostro Matched and FMSG Hold as tentative Day2 scope.
BCS and Egypt retain a separate status model.

Sources: [original lines 1–22](../../../evidence/sources/sha256/7f3e2a5d118de2e0678431263bb9f4391aa4df0011ac58c3e78d01b520c12d82.md#L1-L22).

### Precheck and payment generation intent

Prechecks use currency calendars, active versions, and currency cutoffs before materialization.
READY with no substatus waits for release cutoff before payment generation.
The payment design routes MT or converted MX to the FM SWIFT Gateway.
The gateway communicates with AMH or SCPAY and returns acknowledgements.

These documents describe orchestration responsibilities without proving live configuration.

Sources: [original lines 9–11](../../../evidence/sources/sha256/8b38524860635e161456b4240c06f2273561413b75436803043901c08a1d8ae9.md#L9-L11), [original lines 21–25](../../../evidence/sources/sha256/8b38524860635e161456b4240c06f2273561413b75436803043901c08a1d8ae9.md#L21-L25), [original lines 31–33](../../../evidence/sources/sha256/8b38524860635e161456b4240c06f2273561413b75436803043901c08a1d8ae9.md#L31-L33), [original lines 11–11](../../../evidence/sources/sha256/97226b3c39ebbcb4be4ac414c156ad2b656ad04bc0629dd2cc9ec3352d5efae9.md#L11-L11), [original lines 15–15](../../../evidence/sources/sha256/97226b3c39ebbcb4be4ac414c156ad2b656ad04bc0629dd2cc9ec3352d5efae9.md#L15-L15), [original lines 18–20](../../../evidence/sources/sha256/97226b3c39ebbcb4be4ac414c156ad2b656ad04bc0629dd2cc9ec3352d5efae9.md#L18-L20).

### Stamping and last-mile controls

Stella IRS coupons wait for another leg when received cashflow count is below the expected count.
Murex pending-fixing cashflows use the pending-fixing indicator, excluding withdrawals.
SSI matching uses entity, product specificity, and primary preference in this overview.
Its general order must be reconciled with the country-specific selection contract.

The last-mile proposal blocks prior sends and matching payment economics.
Its economic-check description and example query differ on trade identity.

Sources: [original lines 13–16](../../../evidence/sources/sha256/62c7b1cbb5b7240618cdc110113e69cd8c3d26e6a0c3bcea5682de3fa1b9f2e0.md#L13-L16), [original lines 21–25](../../../evidence/sources/sha256/62c7b1cbb5b7240618cdc110113e69cd8c3d26e6a0c3bcea5682de3fa1b9f2e0.md#L21-L25), [original lines 11–12](../../../evidence/sources/sha256/98270609f797c85a3c3e3f482c08c82f8bac86a0ec8fca22a27358f4f6fd7507.md#L11-L12), [original lines 17–18](../../../evidence/sources/sha256/98270609f797c85a3c3e3f482c08c82f8bac86a0ec8fca22a27358f4f6fd7507.md#L17-L18), [original lines 21–23](../../../evidence/sources/sha256/98270609f797c85a3c3e3f482c08c82f8bac86a0ec8fca22a27358f4f6fd7507.md#L21-L23), [original lines 12–12](../../../evidence/sources/sha256/e088ccc338da682e1e0640a1c685a43444a85c1fbf36ecf9e7cec4d248e26c70.md#L12-L12).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which exception matrix, authority limits, and Day1/Day2 controls govern current operation?
- What exact last-mile economic uniqueness and override contract is approved?
- Which expected-count and SSI selection scopes are approved?
