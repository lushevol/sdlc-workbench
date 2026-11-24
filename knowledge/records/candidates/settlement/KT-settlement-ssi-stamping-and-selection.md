---
type: KnowledgeTopic
id: KT-settlement-ssi-stamping-and-selection
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/SSI Stamping Notification/FMRP - SSI Stamping Flow/Compatibility design
    for multiple entities/page.md
  revision: sha256:0cff366b1e6e5617204d498d84f83ea41b38dc0c995e8712a28cb26507f89400
  sha256: 0cff366b1e6e5617204d498d84f83ea41b38dc0c995e8712a28cb26507f89400
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/SSI Stamping Notification/FMRP - SSI Stamping Flow/Trade SSI Stamping
    - Product templates/page.md
  revision: sha256:86ab80928e977ca334ba672abffcd28df869b9a01fc7b678cb63c6b846f6abd6
  sha256: 86ab80928e977ca334ba672abffcd28df869b9a01fc7b678cb63c6b846f6abd6
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/SSI Stamping Notification/FMRP - SSI Stamping Flow/Trade Strategic
    SSI Stamping Tech Design/page.md
  revision: sha256:75c001018f909d0a620323cdc9b86800b0ebc09b7fcb74efb3cf49c3fe004d43
  sha256: 75c001018f909d0a620323cdc9b86800b0ebc09b7fcb74efb3cf49c3fe004d43
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/SSI Stamping Notification/FMRP - SSI Stamping Flow/Vostro SSI Best
    Matching - UK Cashflow Migration/page.md
  revision: sha256:e2db13b96409d370d158e0c59343b73f47860ba6cb28680c61de9d91ab6044ed
  sha256: e2db13b96409d370d158e0c59343b73f47860ba6cb28680c61de9d91ab6044ed
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/SSI Stamping Notification/FMRP - SSI Stamping Flow/page.md
  revision: sha256:dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28
  sha256: dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/SSI Stamping Notification/SSI Notification Flow/page.md
  revision: sha256:f7610dcf7c4e86b4887e5cc0a98dac8f066d606a9161c513faf6e3bd21196652
  sha256: f7610dcf7c4e86b4887e5cc0a98dac8f066d606a9161c513faf6e3bd21196652
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/SSI Stamping Notification/Trade Cashflow SSI Stamping on Uber Message/page.md
  revision: sha256:38ed6b7743166a3685ad045cec32a9bc94edff364239b6b9c31fa47b2c546208
  sha256: 38ed6b7743166a3685ad045cec32a9bc94edff364239b6b9c31fa47b2c546208
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/SSI Stamping Notification/FMRP - SSI Stamping Flow/SSI Stamping Tech
    Design-Egypt/page.md
  revision: sha256:765d5de5c9a3008124b334f133524ea636587d2f948e604c8aef4d24e307a406
  sha256: 765d5de5c9a3008124b334f133524ea636587d2f948e604c8aef4d24e307a406
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:57:30.629131+08:00'
verified: []
scope: Combined source-specific trade and cashflow SSI query, selection, notification,
  correction, and interface proposals.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which trade-to-cashflow inheritance and CDUPS publication contract is approved?
- Which entities, products, and effective dates use branch-first Vostro selection?
- Which exact notification matrix and trade identity apply to refresh?
- Confirm current regional selection authority, CFI path and effective source precedence.
- Resolve conflicting PartyA/PartyB sell-side missing-Nostro results.
- Resolve CDUPS notification wording, exact transport/response contract and currency-pair
  fallback/replay.
- Resolve blank/both-bound date filters, date timezone and old-SSI deletion behavior.
- Confirm payment-exception direction changes and complete maker/checker editability
  table.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Trade and cashflow SSI stamping and selection

## Scope

Combined source-specific trade and cashflow SSI query, selection, notification, correction, and interface proposals.

## Summary

Sources define historical SSI designs with unresolved authority, regional scope, interface, and inheritance conflicts.

## Documented knowledge

### Strategic trade query

The strategic query expects the latest trade snapshot to match the requested trade ID and major version.
The GraphQL request selects the requested fields.
The response populates only those requested fields.
The historical fallback queries all fields.

Sources: [original lines 3–9](../../../evidence/sources/sha256/75c001018f909d0a620323cdc9b86800b0ebc09b7fcb74efb3cf49c3fe004d43.md#L3-L9), [original lines 40–40](../../../evidence/sources/sha256/75c001018f909d0a620323cdc9b86800b0ebc09b7fcb74efb3cf49c3fe004d43.md#L40-L40).

### Scoped Vostro selection change

The proposal retains existing matching for CN, including HEFEI, SG, IN, MY, AG, EG, SA, and NP.
It also retains existing matching when the original source is LOANIQ.
The new branch-first scope lists UK, HK, TW, and TAIPEI.
New entities and products require separate assessment.

The new algorithm drops global candidates when branch-specific candidates exist.
It then prefers the most granular product and primary instruction.

Sources: [original lines 15–32](../../../evidence/sources/sha256/e2db13b96409d370d158e0c59343b73f47860ba6cb28680c61de9d91ab6044ed.md#L15-L32).

### Notification eligibility

New, amended, or reactivated instructions can restamp specified WAITING/PendingOperator exceptions.
These include MissingVostro, MultiVostro, NostroVsVostroMismatch, and SecondaryVostro.
The listed PendingVerification cases and AdhocSI remain ineligible.
Good system-assigned Vostro in WAITING or READY is eligible.

Deletion or deactivation affects assigned instructions or listed MultiVostro candidates.
Failed restamping requires fresh maker input for PendingOperator.

Sources: [original lines 3–33](../../../evidence/sources/sha256/f7610dcf7c4e86b4887e5cc0a98dac8f066d606a9161c513faf6e3bd21196652.md#L3-L33).

### Notification match scope

Notification matching uses counterparty FMID, currency, and compatible CFI generality.
The examples permit a higher or equal generality match.
Branch-specific instructions restrict the affected branch.
Global instructions query all branches.

Sources: [original lines 3–33](../../../evidence/sources/sha256/f7610dcf7c4e86b4887e5cc0a98dac8f066d606a9161c513faf6e3bd21196652.md#L3-L33).

### Central stamping proposal

The Uber proposal centralizes trade and cashflow SSI stamping.
It accepts a unique trade ID and version instead of a full Uber request.
The product template stamps buy-currency Nostro and sell-currency Vostro plus Nostro.
Its cashflow flow queries the latest major-version trade stamp.

Its refresh and approved ad-hoc flows restamp the corresponding trade.
Publication protocol and trade-to-cashflow inheritance remain unresolved against the separate agreement.

Sources: [original lines 1–5](../../../evidence/sources/sha256/38ed6b7743166a3685ad045cec32a9bc94edff364239b6b9c31fa47b2c546208.md#L1-L5), [original lines 8–14](../../../evidence/sources/sha256/38ed6b7743166a3685ad045cec32a9bc94edff364239b6b9c31fa47b2c546208.md#L8-L14), [original lines 25–60](../../../evidence/sources/sha256/38ed6b7743166a3685ad045cec32a9bc94edff364239b6b9c31fa47b2c546208.md#L25-L60).

### Trade and cashflow separation

The product-template agreement places trade and cashflow stamping in a central service. It links their results but explicitly rejects cashflow inheritance from trade stamping. CDUPS queries the latest cashflow result for fixing notices and calls again for trade events. Refresh and adhoc changes are not published to CDUPS in the listed subitems. The preceding notification wording remains ambiguous. No precedence over other SSI designs is established.

[Source 10, lines 1-5](../../../evidence/sources/sha256/86ab80928e977ca334ba672abffcd28df869b9a01fc7b678cb63c6b846f6abd6.md#L1-L5)

### CDUPS request and response contract

The request requires nonnull string fields for trackingId, tradeId, majorVersion, asOf, effective, requestDate, bookingEntityFmId, counterpartyFmId, cfiCode, settlementMethod and settlementType. Mapped trade fields carry key and value; their pair validates the request. Trade_Id links records. The legs array requires currency and payerPartyReference. settlementType is hardcoded Cash. The response returns nonnull per-leg currency, payerPartyReference, Vostro and Nostro results. Vostro outcomes are SUCCESS, MULTI_VOSTRO_ERROR and MISSING_VOSTRO_ERROR. Nostro adds DEFAULT_NOSTRO and MULTI_NOSTRO_ERROR. HTTP200 includes Success/default Nostro;400 covers validation or missing trade.500/internal errors and timeouts require at least three retries, three minutes apart, retaining trade ID and major version. No populated sample identifiers are retained.

[Source 10, lines 8-26](../../../evidence/sources/sha256/86ab80928e977ca334ba672abffcd28df869b9a01fc7b678cb63c6b846f6abd6.md#L8-L26) [Source 10, lines 28-37](../../../evidence/sources/sha256/86ab80928e977ca334ba672abffcd28df869b9a01fc7b678cb63c6b846f6abd6.md#L28-L37) [Source 10, lines 60-67](../../../evidence/sources/sha256/86ab80928e977ca334ba672abffcd28df869b9a01fc7b678cb63c6b846f6abd6.md#L60-L67)

### Declared testing scope

The product-template testing scope includes FX Forward, Spot, NDF, Swap and VanillaOption; five IRSwap variants; four CrossCurrency variants; and cash/physical precious-metal spot-forward. Events include New, Amendment, Cancel, Novation, Terminations and Undo. VanillaOption additionally lists Exercice and Expire. LoanDeposit is struck through. These are test-scope expectations, without executed results.

[Source 10, lines 69-91](../../../evidence/sources/sha256/86ab80928e977ca334ba672abffcd28df869b9a01fc7b678cb63c6b846f6abd6.md#L69-L91)

### Multi-entity currency-pair proposal

The compatibility proposal targets local-currency utilization for SA, NP and EG, configurable for later entities. Group enrichment requires a supported FX spot/forward/swap taxonomy and exactly two payment currencies. Otherwise, do not enrich the pair. With one Vostro, FXBRREC plus an existing currency pair queries Nostro using that pair; otherwise follow China logic. Missing/multiple Vostro uses primary Nostro with the pair when present. The proposal compares group enrichment against an SSI-service TDS3 query. Missing legs, pair errors, missing Nostro fallback and replay exceptions remain open. The TDS3 option is source-described as slower; no measured performance evidence exists.

[Source 6, lines 7-13](../../../evidence/sources/sha256/0cff366b1e6e5617204d498d84f83ea41b38dc0c995e8712a28cb26507f89400.md#L7-L13) [Source 6, lines 16-18](../../../evidence/sources/sha256/0cff366b1e6e5617204d498d84f83ea41b38dc0c995e8712a28cb26507f89400.md#L16-L18) [Source 6, lines 29-40](../../../evidence/sources/sha256/0cff366b1e6e5617204d498d84f83ea41b38dc0c995e8712a28cb26507f89400.md#L29-L40) [Source 6, lines 44-49](../../../evidence/sources/sha256/0cff366b1e6e5617204d498d84f83ea41b38dc0c995e8712a28cb26507f89400.md#L44-L49)

### Trade lookup and regional selection

Trade stamping first queries Vostro, then uses its settlement means/account for Nostro. A blank query falls back to default Nostro; absent Vostro uses legal entity plus currency. The main non-UK sequence tries CFI granularity of first three characters, first two, then second character only. It next ranks country-primary, global-primary, country-secondary, global-secondary. The UK London/SSTL sequence instead selects branch before CFI and primary preference. It drops global candidates when branch-specific candidates exist. Query predicates include branch/global, currency, CFI hierarchy, counterparty, debit/credit, CASH settlement type, settlement-method/FEDWIRE alternatives, and Active/New/Update statuses. A26June2026 note changes CFI_Code to Financial_Instrument_Code. Populated examples do not define universal configuration.

[Source 7, lines 4-17](../../../evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L4-L17) [Source 7, lines 27-48](../../../evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L27-L48)

### Trade response conflicts

The main flow says missing/multiple Vostro plus missing Nostro uses Please advise for both parties. Its good-Vostro/missing-Nostro row enriches PartyA but leaves PartyB as Please advise. The Egypt response table instead enriches PartyB and leaves PartyA To Be Advise for unique Vostro with missing/multiple Nostro. With default Nostro and absent/multiple Vostro, Egypt enriches PartyA and leaves PartyB Please advise. A unique Nostro/Vostro pair enriches both. Buy-side missing/multiple Nostro is blank/To Be Advise; unique Nostro enriches PartyA. These conflicting sell-side outputs require owner resolution; no current party mapping is selected.

[Source 7, lines 10-17](../../../evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L10-L17) [Source 8, lines 749-769](../../../evidence/sources/sha256/765d5de5c9a3008124b334f133524ea636587d2f948e604c8aef4d24e307a406.md#L749-L769)

### Egypt interface scope

The Egypt design exposes POST trade enrichment with tracking ID, trade ID, product type and base64 trade SCBML. Single-leg versus near/far-leg results depend on product. Its HTTP200 codes distinguish unique pay/receive stamping;400 identifies missing/default-Nostro, invalid-data and undefined-scenario outputs;500 identifies stamping I/O errors. Per-result values include SUCCESS, missing/multiple Vostro/Nostro and DEFAULT_NOSTRO. It marks notification events out of scope and XML attribute definitions open. Currency plus MAIN is its source-labeled default-Nostro resolution. This is a separate interface design, not a replacement CDUPS contract.

[Source 8, lines 7-15](../../../evidence/sources/sha256/765d5de5c9a3008124b334f133524ea636587d2f948e604c8aef4d24e307a406.md#L7-L15) [Source 8, lines 17-37](../../../evidence/sources/sha256/765d5de5c9a3008124b334f133524ea636587d2f948e604c8aef4d24e307a406.md#L17-L37) [Source 8, lines 777-786](../../../evidence/sources/sha256/765d5de5c9a3008124b334f133524ea636587d2f948e604c8aef4d24e307a406.md#L777-L786)

### Payment exception distinctions

Missing Vostro on pay, multiple Vostro on pay/receive, and account mismatch require maker/checker correction. Primary Nostro is displayed; forms validate and compare account/means. A unique secondary Vostro creates a checker-only exception; rejection returns to maker with AdhocSI. Receive with missing Vostro and primary Nostro has no SSI exception. Good stamping can enter adhoc through maker action or checker rejection. Adhoc requires dual-blind matching; pay validates both Vostro/Nostro, receive validates only Nostro. Missing-Nostro handling distinguishes pay from receive and missing from unique Vostro. In the receive/missing-Vostro path, no account/means comparison is required. Source wording for Multi Nostro and blank/form behavior remains inconsistent with later tables.

[Source 7, lines 21-25](../../../evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L21-L25)

### Correction identity and layout

Missing or multiple values start blank. The same maker/checker sees their prior submission/rejection values; a different user sees initial values. Vostro-related exceptions make Vostro editable by default. Nostro-related exceptions make Nostro selectable by default. Mismatch/adhoc starts with Vostro editable and Nostro selectable only through Edit. The detailed table contains conflicting good-stamping Edit-button rows and incomplete Secondary/Adhoc cells. Preserve those gaps rather than inventing a complete editability matrix.

[Source 7, lines 50-84](../../../evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L50-L84)

### Effective-date proposal

The proposal adds Start_EffectiveDate, End_EffectiveDate and Core_EffectiveDate. An end-dated old SSI retains its ID; its replacement uses an _ED suffix. The source proposes deleting the old SSI at the replacement start date, without a new start-date notification. First queries and Vostro exception candidates apply date filtering. An SSI+ update identifies impacted cashflows and retriggers stamping. The pseudocode first accepts end-dated SSI when VD<=end, otherwise rejects it; only then considers start date and VD>=start. It repeats Start_EffectiveDate in its blank-date branch. Both-bound handling, timezone, deletion and refresh completeness remain unresolved. These are proposed storage/filter semantics, not verified source behavior.

[Source 7, lines 150-161](../../../evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L150-L161) [Source 7, lines 186-194](../../../evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L186-L194) [Source 7, lines 196-233](../../../evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L196-L233)

## Connections

The source clauses connect trade queries, regional selection, cashflow exceptions, and CDUPS responses.
The Uber stamping proposal conflicts with the separate product-template no-inheritance agreement.
No source precedence or effective rollout is inferred.

## Evidence limits

The four lane1 identities received full selected-range review.
Lane2 coverage remains partial exactly as recorded in its source review.
The long main-flow wire mappings, bank-scenario tables, images, and color-dependent PvB rule remain incomplete.
This combined review does not advance either lane to broader source completion.
No current policy approval, implementation, execution, deployment, or acceptance is established.

## Open questions

Owner: unknown.

- Which trade-to-cashflow inheritance and CDUPS publication contract is approved?
- Which entities, products, and effective dates use branch-first Vostro selection?
- Which exact notification matrix and trade identity apply to refresh?
- Confirm current regional selection authority, CFI path and effective source precedence.
- Resolve conflicting PartyA/PartyB sell-side missing-Nostro results.
- Resolve CDUPS notification wording, exact transport/response contract and currency-pair fallback/replay.
- Resolve blank/both-bound date filters, date timezone and old-SSI deletion behavior.
- Confirm payment-exception direction changes and complete maker/checker editability table.
