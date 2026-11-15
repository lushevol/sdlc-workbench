---
type: KnowledgeTopic
id: KT-settlement-cpn-netting
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-0afd5f6c09f83a9f3e58ca68
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/CPN Business Scenario.md
  revision: sha256:007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf
  sha256: 007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf
- id: SRC-7ed08e4e144d25600965ee0a
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/CPN Business Scenario/page.md
  revision: sha256:007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf
  sha256: 007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf
- id: SRC-1d38a411947fac07a0f30f7c
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Netting/CPN Business Scenario.md
  revision: sha256:007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf
  sha256: 007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf
- id: SRC-34814f70109c8256a8b7e131
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/CPN Tech Design - Draft for now.md
  revision: sha256:93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f
  sha256: 93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f
- id: SRC-f636dc62a1f888f5963a8965
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/CPN Tech Design - Draft for now/page.md
  revision: sha256:93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f
  sha256: 93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f
- id: SRC-dd63a6adce0cb8ee0d8332dc
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Netting/CPN Tech Design - Draft for now.md
  revision: sha256:93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f
  sha256: 93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f
generated:
  by: agent:codex
  at: '2026-11-15T09:07:38Z'
verified: []
classification: settlement
scope: Historical China Day 1 cross-product netting scenarios and the proposed CPN lifecycle in Payment Lake.
summary: The proposals describe eligibility, manual netting review, Force Gross, and release-dependent recovery. Exact applicability and conflicting state and action labels remain open.
related:
- KT-settlement-auto-netting
- KT-settlement-cashflow-identity-and-stella-write-back
open_questions:
- Which edition of the ad hoc action matrix applies to Projected, Queued, Pending, and Validated components?
- Does Reviewed precede Pending Release or describe the same approved resultant stage in a different state field?
- Which corrected example establishes the ad hoc preview state and approved resultant ID?
- Which entity, product, and release scopes apply to the historical proposals?
- Which order selects the first component for settlement instructions and product mapping?
- Which role approves Force Gross and which operations are permitted after cancellation?
---
# CPN eligibility, manual netting, and review

## Scope

This topic covers historical cross-product netting (CPN) proposals for China Day 1 and Payment Lake.
The two revisions contain a scenario catalogue and nine proposed technical lifecycle scenarios.

## Summary

The proposals validate a common netting key and hold the resultant for checker review.
Release status determines how the technical draft handles an amendment or cancellation.
Exact business scope, status labels, and review permissions still need confirmation.

## Documented knowledge

### China Day 1 and source routing

The China Day 1 scope names derivatives and excludes Razor cashflows. The proposed Murex 2.11 path adds China to existing CPN static and routes eligible cashflows to RATAN. Untagged Murex clients normally settle gross. A manual queue can route selected cashflows to RATAN for ad hoc CPN. [Murex eligibility](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L12-L14) [Ad hoc route](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L18).

For linear rates moving to FMRP, check the SCI flag, counterparty/currency/product static, and currency exclusions in that order. The business examples use a client agreement to select products for netting. A client or product outside the example agreement stays gross unless an ad hoc request applies. [FMRP checks](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L20-L28) [Agreement examples](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L50-L55) [Initial flows](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L57-L60).

The scenario and technical matrices put scheduled CPN outside Day 1. A separate agreement section describes operator selection or a configured future schedule for eligible flows. Treat the scheduled example as a proposed option with unresolved applicability. Product auto-netting appears as a distinct catalogue scenario. [Scenario matrix](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L3) [Eligibility and action](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L40-L45) [Technical scope](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L17-L20).

### Manual and ad hoc netting

The business proposal validates equal booking entity, counterparty, currency, and value date. Released or Settled components fail validation. Calculate the resultant using pay/receive direction. Use a common netting ID to link components and resultant. The resultant requires a different checker from the maker. [Validation and resultant](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L46-L47).

The business workflow tags regular eligible flows `Pending / Pending Netting`. A client request before cutoff can include gross STP flows shown as `Validated / Pending Release`. The ad hoc example confirms the selected cashflows with the client. It uses the same preview, submission, and checker flow as the regular example. The ad hoc preview table already labels components Netted, so matrix labels alone cannot establish a state change before submission. [Client request](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L48) [Ad hoc example](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L67-L74).

The business design proposes inheriting the first component's settlement instruction. It also proposes using the first component's product for SSI stamping. One example assigns the product shown on a later row. Component ordering and the relationship between these two inheritance rules remain open. [Settlement instruction](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L38) [Product rule and example](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L47) [Regular preview](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L61).

The business workflow previews components and a projected resultant. Submission marks components Netted and creates a Queued resultant with a gross classification. The resultant then enters NSTP as `Pending / Netting Review`. The checker can accept it or restore the original components. The accepted result enters `Validated / Pending Release`. [Business review sequence](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L61-L65).

The technical design routes Murex and Stella cashflows into Payment Lake. SCBML feeds the settlement workflow, whose eligibility task marks the CPN population. Netted components leave the blotter and bypass subsequent workflow tasks. The new resultant moves from Queued to `Pending / Netting Review`. The checker example ends in `Validated / Reviewed`. The relationship between Reviewed and the business scenario's Pending Release needs confirmation. [Technical CPN sequence](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L35-L41).

The technical action matrix places Ad-hoc NET under Projected/Queued and shows NA in the next columns. Scenario 1 includes Projected, Queued, Pending, and Validated together. Its approval prose and table identify different resultant IDs. Treat these as unresolved example differences before defining the GUI or approval contract. [Action matrix](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L8-L16) [Mixed-state example](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L22-L29).

### Force Gross and manual un-net

Operators can select eligible Pending CPN components for Force Gross. The draft moves them to Force Gross Review before approval. The description names a maker review, while its next step names a checker approving to `Validated / Reviewed`. The reviewer rule remains open. [Force Gross](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L45-L51).

The technical draft proposes full manual un-net on a Pending or Validated resultant before release. The maker submits it for Un-Net Review. Checker acceptance marks the resultant Dead and requeues components for eligibility and possible manual netting. The draft excludes partial un-net and net-of-net. It refers to existing production behavior for incremental amendments without defining that behavior. [Action matrix](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L8-L20) [Before review](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L57-L61) [After review](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L67-L71).

### Component amendment and cancellation

Before release or settlement, the technical scenarios propose automatic un-net when a component changes. The old resultant becomes Dead. The workflow reruns eligibility on the latest component versions. Cancellation marks the cancelled component Dead. The cancellation example calls the incoming event an amendment in prose. Its action row offers Netting/Force Gross even though the component is Dead. [Before-release amendment](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L75-L82) [Before-release cancellation](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L109-L116).

After release or settlement, the amendment and cancellation scenarios preserve the original resultant. They create a new reversal with the reversal flag set and an ID link to the original. The reversal waits in NSTP Release for operations. Remaining eligible components return to processing. The cancellation example again says amendment in prose and shows an action on the Dead component. MTx92 generation is a future option in the draft. [Released amendment](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L86-L105) [Released cancellation](../../../evidence/sources/sha256/93f28349f407c671d4b99aa65395a7a7c11f318c793cfb203a8ab9153fd6534f.md#L120-L139).

### Related catalogue proposals

The catalogue ranks product auto-netting, CLS, general netting, and ad hoc netting in that order where cases overlap. It lists scope and routing examples for gross, CFETS, BIC, LCM, CCIL, cross-FXMM/derivative, combined, tenure, and currency-pair flows. Those rows carry their own scope flags and open predicates. [Catalogue and precedence](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L3) [Priority example](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L9).

The same source requests automatic blotter refresh and removal of the DQSL result count cap. It proposes separate general and ad hoc cutoffs by entity and currency. The DVP discussion distinguishes gross FX DVP, a request to consider FX DVP netting, and commodity derivative release after bullion confirmation. These catalogue requests need their own scope and acceptance decisions. [UI and cutoffs](../../../evidence/sources/sha256/007a5034111e9dfccb1fb02bc25f06e1af45c1f1c727a4fb94acc89ab8fb70cf.md#L7-L11).

## Connections

The scheduled rule and execution key are covered in [Cash Settlement auto-netting](KT-settlement-auto-netting.md).
The [cashflow identity topic](KT-settlement-cashflow-identity-and-stella-write-back.md) covers the broader ID and Stella write-back contracts.
The CPN netting linkage and proposed reversals have their own stated scope.

## Evidence limits

The catalogue and technical design describe historical proposals. Current authority, rollout, and runtime behavior need separate evidence.
Four retained source identities represent two distinct revisions. The static table illustration is unavailable.
The scenarios contain inconsistent example values and state labels. Example IDs, versions, and amounts are illustrative.

## Open questions

The owner is unknown.

- Which edition of the ad hoc action matrix applies to Projected, Queued, Pending, and Validated components?
- Does Reviewed precede Pending Release or describe the same approved resultant stage in a different state field?
- Which corrected example establishes the ad hoc preview state and approved resultant ID?
- Which entity, product, and release scopes apply to the historical proposals?
- Which order selects the first component for settlement instructions and product mapping?
- Which role approves Force Gross and which operations are permitted after cancellation?
