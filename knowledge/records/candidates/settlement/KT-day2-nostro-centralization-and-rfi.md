---
type: KnowledgeTopic
id: KT-day2-nostro-centralization-and-rfi
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-bfc3930baa7ccb902e5fed40
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Nostro Centralization/page.md
  revision: sha256:4e9b71cc57b322fa06b6680a12f321998dcf77e8db73dbf5654481a3e86c16d2
  sha256: 4e9b71cc57b322fa06b6680a12f321998dcf77e8db73dbf5654481a3e86c16d2
- id: SRC-d1d89327eef7ed58d51c2b45
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Nostro Maintenance By Uploading CSV File/page.md
  revision: sha256:c45abdb13faf9d810d51d81e798b61bd5f193aae3e0015b853997a45cc44a551
  sha256: c45abdb13faf9d810d51d81e798b61bd5f193aae3e0015b853997a45cc44a551
- id: SRC-c703e47bbc53aee2cd3c0e28
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/RFI Nostro stamping based on Portfolio/Cashflow
    Dedicated Nostro Stamping Design(like RFI STRATEGY etc.)/page.md
  revision: sha256:40e22b2943cc547fc99e2161cfc679967ff2b4701bb3bd753838a30060427be9
  sha256: 40e22b2943cc547fc99e2161cfc679967ff2b4701bb3bd753838a30060427be9
- id: SRC-72ff613174f1a87997730f21
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/RFI Nostro stamping based on Portfolio/Change
    List and API/page.md
  revision: sha256:8508fd13bbd7b74da017025e7a97c3c898bd9110953f21b31f89224e57aa1ede
  sha256: 8508fd13bbd7b74da017025e7a97c3c898bd9110953f21b31f89224e57aa1ede
- id: SRC-866ba45098b31b45edf5cdf4
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/RFI Nostro stamping based on Portfolio/page.md
  revision: sha256:c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954
  sha256: c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954
classification: settlement
scope: Nostro centralization, upload, and dedicated RFI selection
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- OPS-A-KT-SSI-AND-NOSTRO
- KT-ratan-entity-and-currency-onboarding-controls
open_questions:
- 'KDQ-9afac8fdaf: Which SSI+ query/event schemas, refresh population, and historical-ID
  migration rules govern centralization?'
- 'KDQ-f8b69a6be1: Which RFI fallback, SI mismatch, scope, uniqueness, and migration
  rules govern?'
- 'KDQ-08b65ee5de: Which effective accounting/static refresh and deduplication rules
  apply?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:55:24.862084+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Nostro centralization, upload, and dedicated RFI selection

## Scope

Nostro centralization, upload, and dedicated RFI selection.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### L3-NOSTRO-01 — Centralization target

NAMS consolidation proposes Data Ops maintenance in SSI+. RATAN must query SSI+ for cashflow, trade, and accounting Nostro stamping. New, Update, and Delete notifications must trigger refresh. Schemas and mappings remain open, including NOS versus Nostro terminology. Historical cashflow-linked Nostro IDs require a migration decision. RFI portfolio mapping and Keystone are related work, without proven rollout.

[Original evidence](../../../evidence/sources/sha256/4e9b71cc57b322fa06b6680a12f321998dcf77e8db73dbf5654481a3e86c16d2.md#L1-L7). [Original evidence](../../../evidence/sources/sha256/4e9b71cc57b322fa06b6680a12f321998dcf77e8db73dbf5654481a3e86c16d2.md#L11-L13). [Original evidence](../../../evidence/sources/sha256/4e9b71cc57b322fa06b6680a12f321998dcf77e8db73dbf5654481a3e86c16d2.md#L15-L17).

### L3-NOSTRO-02 — Atomic CSV import proposal

POST /v2/static/nostros/upload accepts a CSV file and directConfirm. Invalid content rejects the whole file. The listed duplicate key combines legalEntityFmId, currency, settlementMeans, settlementAccount, startDate, and endDate. The success response uses status 200 and the uploaded count in errorMessage. The failure example uses status 400 and errorCode 800400117. directConfirm true selects save_confirmed; false selects update_pending. No operator authorization is specified.

[Original evidence](../../../evidence/sources/sha256/c45abdb13faf9d810d51d81e798b61bd5f193aae3e0015b853997a45cc44a551.md#L1-L10).

### L3-NOSTRO-03 — Dedicated lookup architecture

The dedicated-Nostro design finally selects memory plus database lookup, despite stating a preference for memory-only. It prefers a child table with jsonb for dedicated data. New Nostro types still require user matching conditions, code, and mapping changes. This is not configuration-only support for arbitrary types. Compare returned dedicated Nostro IDs for current New and Withdrawal messages to classify amendment changes. Technical failure in a NonEcoAmend group must become economic; other named amendment branches retain their stated handling.

[Original evidence](../../../evidence/sources/sha256/40e22b2943cc547fc99e2161cfc679967ff2b4701bb3bd753838a30060427be9.md#L1-L65). [Original evidence](../../../evidence/sources/sha256/40e22b2943cc547fc99e2161cfc679967ff2b4701bb3bd753838a30060427be9.md#L79-L94). [Original evidence](../../../evidence/sources/sha256/40e22b2943cc547fc99e2161cfc679967ff2b4701bb3bd753838a30060427be9.md#L96-L110).

### L3-NOSTRO-04 — Conflicting technical decisions

Technical Q8 says no RFI match produces Missing Nostro; the functional view instead falls back to ordinary stamping. Technical Q11 removes Vostro/Nostro means/account matching for RFI; the functional view retains SI mismatch. Early technical questions include five entrypoints, while later answers exclude trade stamping. KRO and KOR literals differ. Early nostrumType/nostroKey uniqueness differs from the final five-factor rule. Q28 says no migration; Q31 requires DEFAULT population and conversion of existing RFI records. Retain these alternatives until owner review.

[Original evidence](../../../evidence/sources/sha256/40e22b2943cc547fc99e2161cfc679967ff2b4701bb3bd753838a30060427be9.md#L1-L65). [Original evidence](../../../evidence/sources/sha256/40e22b2943cc547fc99e2161cfc679967ff2b4701bb3bd753838a30060427be9.md#L79-L94). [Original evidence](../../../evidence/sources/sha256/40e22b2943cc547fc99e2161cfc679967ff2b4701bb3bd753838a30060427be9.md#L96-L110).

### L3-NOSTRO-05 — Proposed service interfaces

Static service adds NostroType and dedicated information, findDedicated for SSI, and findDedicateds for group amendment classification. Empty query NostroType fetches all types. Lifecycle domain events and /v2/ratan/cashflow/move/status responses include NostroType. Query detail exposes Nostro_Type and Dedicated. Adhoc maker/checker fitNostro includes nostroType and dedicatedPortfolio. MT210 tag25 applies when currency is KRW and the correspondent account exists. Example account and address literals are excluded.

[Original evidence](../../../evidence/sources/sha256/8508fd13bbd7b74da017025e7a97c3c898bd9110953f21b31f89224e57aa1ede.md#L5-L12). [Original evidence](../../../evidence/sources/sha256/8508fd13bbd7b74da017025e7a97c3c898bd9110953f21b31f89224e57aa1ede.md#L22-L23).

### L3-NOSTRO-06 — Functional RFI selection and exceptions

The London RFI proposal stamps dedicated Korea Nostro by portfolio and currency. Portfolio is mandatory for RFI records; Primary is disabled. Duplicate checking uses booking entity, currency, means, account, and Nostro type. Query with booking entity, currency, and portfolio. Stamp a single match; multiple matches generate Missing Nostro; no match follows the ordinary process. Keep Vostro logic unchanged and prevent it from overwriting the selected Nostro. SI mismatch remains required when Vostro/Nostro means or accounts differ.

[Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L1-L4). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L6). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L12-L19). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L27-L36). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L38-L42). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L50-L53). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L56).

### L3-NOSTRO-07 — Functional amendment and manual scope

A non-RFI/RFI portfolio change is economic. Indicator lookup technical failure defaults to economic change. Cashflow stamping is in scope; trade stamping stays BAU until the separate strategic solution. Adhoc selection may select an RFI Nostro even for a non-RFI portfolio. Show Nostro Type in selection and cashflow detail. MT210 tag25 takes the Nostro account only for ISO currency KRW. Proposed downstream integration testing is a requirement, without execution evidence.

[Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L1-L4). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L6). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L12-L19). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L27-L36). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L38-L42). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L50-L53). [Original evidence](../../../evidence/sources/sha256/c3f430a1472df88805901bb83d0193abacfc7513b7f08cd98634c41cd9cc3954.md#L56).

## Connections

Related canonical IDs: `OPS-A-KT-SSI-AND-NOSTRO`, `KT-ratan-entity-and-currency-onboarding-controls`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
