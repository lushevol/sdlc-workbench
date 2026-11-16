---
type: KnowledgeTopic
id: KT-settlement-processing-and-exception-controls
version: 2
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
  by: agent:pi-source-finalizer
  at: '2026-11-16T13:37:43Z'
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
previous_version: 1
previous_content_sha256: 9e4ebcd1a7869eb16a9f42a602c1613dcf186cd7c8a5e67b731a165f3a484b77
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

### Named precheck responsibilities

The precheck catalog assigns currency holidays and weekends to `ratanone.ratan_static_cashflow_currency_holiday`, with calendars from RDM.
It assigns active-version checks to `ratanone.ratan_static_activated_version`, shown with alias `rsav`.
It assigns RATAN currency cutoffs to `ratanone.ratan_static_cashflow_currency_cut_off`.
The catalog assigns `RAT_CN_MLZ` materialization from projected to queued status.
These are documented responsibilities. They establish no current table use or scheduled execution.

[Selected table and job catalog](../../../evidence/sources/sha256/8b38524860635e161456b4240c06f2273561413b75436803043901c08a1d8ae9.md#L21-L33)

### Suppression transition

The suppression page specifies `Queued` to `SUPPRESSED` when the cashflow matches a configured suppression rule.
Its cashflow-suppression and SWIFT-suppression effects remain distinct, as described above.

[Selected suppression rules](../../../evidence/sources/sha256/aa26d8534029330abaf84b48a3a4fe84418776af4798ab15fe716baa8b72f026.md#L9-L20)

### Cashflow flags and producer-specific fixing

LIEN placement and LIEN-amount updates require the `LIEN` exception for all trade cashflows, including interest, with maker and checker.
Matching the BIC Netting Static tile sets the BIC net flag to `Y`.
`Cashflow_Amount_USD_Transfered` indicates the equivalent USD amount.
The page assigns this flag to the NSTP high-value check and the automatic inter-entity netting check.

For Blade/Stella IRS, known fixed-leg payments can arrive in advance, probably with `PROJECTED` status.
Floating-leg generation normally follows fixing on VD-2. Settlement expects the net fixed-leg and floating-leg amount for each schedule.
The detailed Stella predicate requires these taxonomy values:

- ` InterestRate:IRSwap:FixedFloat`
- `InterestRate:IRSwap:OIS`
- `InterestRate:IRSwap:FloatFloat`
- `InterestRate:IRSwap:FixedFixed`

The source prints a leading space in the FixedFloat value. It does not establish a normalization rule.
It also requires `Coupon/Fixed` or `Coupon/Float`, and excludes `Withdrawal` events.
It compares RATAN and TDX counts for the same cashflow ID and value date.
A lower RATAN count produces `WAITING + Pending another leg`; otherwise processing continues.
The source spells the comparison system `TDX`. This statement does not normalize that identifier.

The Murex predicate requires `pending_fixing='Y'` and excludes `Withdrawal` events.
It produces the same `WAITING + Pending another leg` status; otherwise processing continues.
The page describes a fixed-leg payment, its reversal after floating fixing, and a replacement net payment with fixing flag `N`.
Stella sends the legs separately for automatic IRS netting.
These are source-specific workflows. They do not establish one universal producer contract.

[Selected flag duties](../../../evidence/sources/sha256/62c7b1cbb5b7240618cdc110113e69cd8c3d26e6a0c3bcea5682de3fa1b9f2e0.md#L13-L16)
[Selected fixing predicates and USD consumers](../../../evidence/sources/sha256/62c7b1cbb5b7240618cdc110113e69cd8c3d26e6a0c3bcea5682de3fa1b9f2e0.md#L21-L25)

### SSI lookup and enrichment duties

The overview obtains Vostro data from SSI+ ES, then matches Nostro data for SWIFT generation.
SSI+ notifications trigger refreshing for pending cashflows under this source's stated scope.
Its Vostro preference is entity before Global, more specific CFI code, then primary SSI.
The source labels these dimensions `branchIdMurex3Id`, `CFI_code` and `Is_Default_SSI`.
The existing country-specific qualification above remains necessary.

For RFI, the Nostro lookup uses portfolio and currency.
The trade-based lookup uses legal-entity FMID, currency, Vostro, settlement means and settlement account.
Users can request ad-hoc changes after SSI+ stamping.
For MT103, address enrichment uses the SCI cache first and an ad-hoc SCI call when the cache lacks data.
This lookup description supplies no complete refresh eligibility, tie-breaker or failure contract.

[Selected SSI lookup and enrichment](../../../evidence/sources/sha256/98270609f797c85a3c3e3f482c08c82f8bac86a0ec8fca22a27358f4f6fd7507.md#L11-L23)

### Exception triggers and release control

The exception overview lists pending confirmation or affirmation, SSI stamping, high value, NSTP rules, back value and net/settled-as-gross cases.
It leaves further cases unspecified.
A pending confirmation or affirmation exception can close automatically after the corresponding confirmation or affirmation arrives.
The NSTP task loads predefined rules from service-maintained static data and applies them to cashflow SCBML.
These rules form a blacklist. Matching cashflows remain held for manual review in the cashflow blotter.
The source describes subsequent SWIFT generation according to the requirement. It supplies no general override grant.

[Selected exception overview](../../../evidence/sources/sha256/bb673d577aa8824afc835778505b0e2970f55e645a52e1ce35585d75b97d6e5c.md#L13)

The SWIFT page uses the literal eligibility labels `Ready +NA` and waits for release cutoff.
It assigns cutoff-based MT generation to Control-M job `RAT_CN_HOLD_RELEASE`.
Generation combines cashflow data with Vostro and Nostro SSI data.
When conversion is required, MT converts to MX before delivery to FMSGW. Otherwise FMSGW receives MT.
The source delegates conversion conditions to linked configuration. Those conditions remain uninspected.
The gateway's AMH/SCPAY and ACK/NACK responsibilities remain distinct from generation.

[Selected SWIFT responsibility and release flow](../../../evidence/sources/sha256/97226b3c39ebbcb4be4ac414c156ad2b656ad04bc0629dd2cc9ec3352d5efae9.md#L11-L20)

### Last-mile identity and economic predicates

The duplicate-send proposal uses cashflow ID, business version, event type and message type.
Its example blocks matching results with `SENT`, `FORCE_RELEASED` or `PENDING_CONFIRMATION` substatus.
The economic description names booking-entity FMID, counterparty FMID, payment amount, payment currency and payment date.
Its example additionally matches trade identity with null-safe equality and excludes the current cashflow ID.
It uses the same three substatus values.
These example predicates preserve the source difference. They do not settle the approved economic-uniqueness or override contract.

[Selected last-mile proposal](../../../evidence/sources/sha256/e088ccc338da682e1e0640a1c685a43444a85c1fbf36ecf9e7cec4d248e26c70.md#L12)

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
