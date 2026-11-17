---
type: Summary
description: "Collects historical settlement exception, suppression, precheck, acknowledgement, and last-mile control descriptions."
doc_type: short
full_text: sources/KT-settlement-processing-and-exception-controls.md
---

> **Candidate/draft only:** These historical control descriptions do not establish current approved operating behavior.

# Settlement Processing and Exception Controls

The selected NSTP design describes exception-specific maker, checker, authority-limit, and auto-resolution rules. Rejected SSI input preserves maker values, and previously netted cashflows require an approver distinct from the unnetting user. A historical table names extra handling above USD 100 million. These limits are source-specific.

Cashflow suppression removes payment and accounting; payment or Swift suppression retains accounting. Manual suppression uses maker-checker, and historical unsuppression stops at value date. Released or settled items cannot be manually failed. The selected China status table distinguishes FMSRE acknowledgement as Released from AMH/SCPAY acknowledgement as Settled, and keeps BCS/Egypt on a separate model.

Precheck uses currency calendars, active versions, and cutoffs. READY cashflows with no substatus wait for release cutoff before payment generation through the FM Swift Gateway. IRS count checks and pending-fixing flags are also described. Last-mile checks block previous sends and matching economics, but the example and query differ on trade identity. None of these statements verifies live configuration or execution.

## Canonical sections

- [Maker-checker exception handling](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#maker-checker-exception-handling)
- [Suppression and failure boundaries](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#suppression-and-failure-boundaries)
- [China status and acknowledgement model](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#china-status-and-acknowledgement-model)
- [Precheck and payment generation intent](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#precheck-and-payment-generation-intent)
- [Stamping and last-mile controls](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#stamping-and-last-mile-controls)


## Related candidate topics

- [[summaries/KT-platform-cashflow-processing-contracts]]
- [[summaries/INT-KT-cashflow-amendment-and-release-controls]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.

## Version 2 source-specific control detail

The precheck catalog assigns holidays and weekends to `ratanone.ratan_static_cashflow_currency_holiday`, using RDM calendars.
Active-version checks use `ratanone.ratan_static_activated_version`, alias `rsav`.
Cutoffs use `ratanone.ratan_static_cashflow_currency_cut_off`.
`RAT_CN_MLZ` materializes projected cashflows to queued status.
These are historical responsibilities, with current table use and execution unverified.
[Named precheck responsibilities](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#named-precheck-responsibilities)

A configured suppression match changes `Queued` to `SUPPRESSED`.
Cashflow suppression and payment/SWIFT suppression retain their different accounting effects.
[Suppression transition](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#suppression-transition)

LIEN placement or amount updates require the `LIEN` exception on all trade cashflows, including interest, with maker and checker.
A BIC Netting Static match sets the BIC net flag to `Y`.
`Cashflow_Amount_USD_Transfered` supplies equivalent USD amounts for NSTP high-value and automatic inter-entity netting checks.
[Cashflow flags and producer-specific fixing](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#cashflow-flags-and-producer-specific-fixing)

Blade/Stella fixed-leg payments can arrive early, probably `PROJECTED`; floating generation normally follows fixing on VD-2.
The source expects the net fixed-leg and floating-leg amount for each schedule.
Its Stella predicate lists ` InterestRate:IRSwap:FixedFloat`, `InterestRate:IRSwap:OIS`, `InterestRate:IRSwap:FloatFloat`, and `InterestRate:IRSwap:FixedFixed`.
The leading space in FixedFloat remains literal, without a normalization rule.
It requires `Coupon/Fixed` or `Coupon/Float` and excludes `Withdrawal` events.
A lower RATAN count than `TDX`, for the same cashflow ID and value date, produces `WAITING + Pending another leg`.
Otherwise processing continues. The source's `TDX` identifier remains unchanged.

Murex separately uses `pending_fixing='Y'`, excludes `Withdrawal`, and produces the same waiting status when that predicate matches.
It describes fixed-leg reversal and replacement net payment with fixing flag `N`; Stella instead sends separate legs for IRS netting.
These producer-specific workflows establish no universal fixing contract.
[Producer predicates](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#cashflow-flags-and-producer-specific-fixing)

The SSI overview queries Vostro through SSI+ ES, then matches Nostro for SWIFT generation.
Its preference is entity before Global, more specific CFI code, then primary SSI.
Its literal dimensions are `branchIdMurex3Id`, `CFI_code`, and `Is_Default_SSI`.
Country-specific selection contracts still require reconciliation.
SSI+ notifications refresh pending cashflows within the overview's stated scope.
RFI lookup uses portfolio and currency; trade lookup uses legal-entity FMID, currency, Vostro, settlement means, and settlement account.
Ad-hoc changes remain available after stamping.
MT103 address enrichment checks SCI cache first, then calls SCI when data is absent.
Refresh eligibility, tie-breakers, and failure behavior remain incomplete.
[SSI lookup and enrichment duties](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#ssi-lookup-and-enrichment-duties)

The exception overview lists confirmation/affirmation, SSI, high-value, NSTP-rule, back-value, and net/settled-as-gross cases, with further cases unspecified.
Corresponding confirmation or affirmation can automatically close its pending exception.
NSTP rules load service-maintained static data and check cashflow SCBML as a blacklist.
A match holds the cashflow for manual review; this description grants no general override.
The SWIFT page uses literal `Ready +NA` eligibility and Control-M job `RAT_CN_HOLD_RELEASE` at release cutoff.
Generation combines cashflow, Vostro, and Nostro data; required conversion changes MT to MX before FMSGW delivery.
Otherwise FMSGW receives MT. Conversion conditions remain in uninspected linked configuration.
AMH/SCPAY and ACK/NACK gateway responsibilities remain distinct.
[Exception triggers and release control](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#exception-triggers-and-release-control)

The duplicate-send proposal uses cashflow ID, business version, event type, and message type.
Its example blocks `SENT`, `FORCE_RELEASED`, or `PENDING_CONFIRMATION` matches.
The economic description compares booking-entity FMID, counterparty FMID, amount, currency, and payment date.
The example additionally uses null-safe trade-identity equality and excludes the current cashflow ID, with the same three substatuses.
This difference leaves economic uniqueness and overrides unresolved.
[Last-mile identity and economic predicates](../../../records/candidates/settlement/KT-settlement-processing-and-exception-controls.md#last-mile-identity-and-economic-predicates)
