---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-profile-authorization-limits",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-b26bb3fb1e5758921cd59572",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Profile USD Limit/page.md",
      "revision": "sha256:28bfe9d36d6dbe31c1d1919d2c05f6de47f6d4413215b356b73a71d27b1281f3",
      "sha256": "28bfe9d36d6dbe31c1d1919d2c05f6de47f6d4413215b356b73a71d27b1281f3",
      "snapshot": "knowledge/evidence/sources/sha256/28bfe9d36d6dbe31c1d1919d2c05f6de47f6d4413215b356b73a71d27b1281f3.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:42:43.141303+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Documented legacy profile USD limits, maintenance control, conversion, and proposed authorization storage.",
  "summary": "Use sourced USD authorization limits for settlement actions without inventing CES role mappings.",
  "related": [
    "KT-settlement-multi-exception-control",
    "KT-settlement-hold-unhold",
    "KT-sdk-and-entitlements",
    "KT-ces-migration-parity"
  ],
  "open_questions": [
    "Which profile limits and action grants are approved for each entity and date?",
    "Who owns the business profile and amount-limit contract during CES migration?",
    "Which FX rate date, EOD tag, precision, and failure handling govern USD conversion?",
    "Was the separate authorization table and hidden-button proposal adopted?"
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Automated checks do not establish complete writing review.",
    "Authority, applicability, and human publication review remain pending."
  ]
}
---
# Settlement profile authorization limits

## Scope

Documented legacy profile USD limits, maintenance control, conversion, and proposed authorization storage.
These isolated proposals require canonical integration and authority review.

## Summary

Use sourced USD authorization limits for settlement actions without inventing CES role mappings.
These documents describe intended responsibilities and proposals. They do not establish current implementation or deployment.

## Documented knowledge

### WF-CF-060

USD profile thresholds constrain checker operations; the source lists clerk below USD 30 million, officer below USD 100 million, lead below USD 1 billion, and manager up to USD 4 billion.

Conditions: Thresholds are maintainable static data rather than immutable universal policy.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 1–13](../../../../knowledge/evidence/sources/sha256/28bfe9d36d6dbe31c1d1919d2c05f6de47f6d4413215b356b73a71d27b1281f3.md#L1-L13)

Limit: Legacy/new RATAN and RAZOR labels do not establish CES ownership or role mappings.

### WF-CF-061

Profile-limit static-data creation, update, and deletion require maker-checker; non-USD payment amounts convert using the Stella FX spot rate with USD as quote currency.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 15–24](../../../../knowledge/evidence/sources/sha256/28bfe9d36d6dbe31c1d1919d2c05f6de47f6d4413215b356b73a71d27b1281f3.md#L15-L24)

Limit: Rate date/eodTag selection and conversion failure handling are not specified by this selected text.

### WF-CF-062

A later proposal stores Profile, Currency, USDConverted, and Limit separately and hides submit/approve when a user lacks the cashflow authorization limit.

Source status: future table/visibility proposal.
[Retained original, lines 26–39](../../../../knowledge/evidence/sources/sha256/28bfe9d36d6dbe31c1d1919d2c05f6de47f6d4413215b356b73a71d27b1281f3.md#L26-L39)

Limit: No exact approved data model, rate timing, or deployed implementation is established.

### Profile identities and action distinctions

The source table includes maker label `FMO_OPS_MKR` and checker labels `FMO_OPS_BOC`, `FMO_OPS_BO`, `FMO_OPS_BOL`, and `FMO_OPS_BOM`.
It also lists separate RAZOR labels; those do not establish interchangeable APIs or CES mappings.
The onshore Middle Office description allows limited netting and cashflow affirmation actions.
The lead's high-risk list includes adhoc netting, amendment/cancellation after release, exceptions at or above USD 100 million, and CPN across FX/derivatives.
Static maker/checker labels are `FMO_STA_MKR` and `FMO_STA_CKR`.
Business-rule maker/approver labels are `FMO_BR_MKR` and `FMO_BR_APR`.
Their table includes USD profile limits, suppression, NSTP and netting rules as business-rule maintenance scope.
These labels and limits require dated applicability confirmation; no current grant is inferred.
[Profile and action proposal](../../../../knowledge/evidence/sources/sha256/28bfe9d36d6dbe31c1d1919d2c05f6de47f6d4413215b356b73a71d27b1281f3.md#L11-L13)

USD payment currency uses the payment amount directly.
Other currencies multiply `Cashflow.Payment_Amount` by Stella's spotRate, with payment currency as base and USD as quote.
The source endpoint is `fx/rates/date/eodTag/baseCurrency/quoteCurrency`; its populated example is not a prescribed rate date or EOD tag.
The proposed separate table fields are Profile, Currency, USDConverted and Limit.
The proposal shows Submit/Approve only when the user has the applicable cashflow limit.
[Conversion and proposed visibility](../../../../knowledge/evidence/sources/sha256/28bfe9d36d6dbe31c1d1919d2c05f6de47f6d4413215b356b73a71d27b1281f3.md#L20-L39)

## Connections

Related proposed or existing records: `KT-settlement-multi-exception-control`, `KT-settlement-hold-unhold`, `KT-sdk-and-entitlements`, `KT-ces-migration-parity`.
The reconciliation file identifies integration overlaps.

## Evidence limits

Only the selected source views were read. Excluded original lines were not opened.
Linked diagrams, attachments, policies, configurations, and external destinations were not inspected.
Documented designs do not establish executed behavior or current rollout.
Source authority and current applicability remain unconfirmed.
No publication approval or business verification is recorded.

## Open questions

Owner: unknown.

- Which profile limits and action grants are approved for each entity and date?
- Who owns the business profile and amount-limit contract during CES migration?
- Which FX rate date, EOD tag, precision, and failure handling govern USD conversion?
- Was the separate authorization table and hidden-button proposal adopted?
