---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-trade-control-expansion-intent",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-1cd16db32872f894934d613b",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Release/Ratan Release Plan 2026/Ratan New Onboarding Checklist 2026/2026_06_27_CHG0991246-Trade-Control-FXO-Manual-Validation/page.md",
      "revision": "sha256:082cebade6e1a2ae48bcc07f09ae389d84bcfc2124f2622daf6626c4265d9f80",
      "sha256": "082cebade6e1a2ae48bcc07f09ae389d84bcfc2124f2622daf6626c4265d9f80",
      "snapshot": "knowledge/evidence/sources/sha256/082cebade6e1a2ae48bcc07f09ae389d84bcfc2124f2622daf6626c4265d9f80.md"
    },
    {
      "id": "SRC-e21f424bee8a6ad206a877f4",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Release/Ratan Release Plan 2026/Ratan New Onboarding Checklist 2026/2026_06_27_CHG0993226_C&A/page.md",
      "revision": "sha256:0d5fe121b5bae684b2f7d1b356fd51d4d981db2d3984b853c66209afdd1aea32",
      "sha256": "0d5fe121b5bae684b2f7d1b356fd51d4d981db2d3984b853c66209afdd1aea32",
      "snapshot": "knowledge/evidence/sources/sha256/0d5fe121b5bae684b2f7d1b356fd51d4d981db2d3984b853c66209afdd1aea32.md"
    },
    {
      "id": "SRC-499b420cc9627072900a0562",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Release/Ratan Release Plan 2026/Ratan New Onboarding Checklist 2026/2026_09_19 CHG1055395 Trade Control New Dashboard/page.md",
      "revision": "sha256:168a7c81850500aa1d6f7153ff7481d81eabb3457305ca6792dd3618043689e9",
      "sha256": "168a7c81850500aa1d6f7153ff7481d81eabb3457305ca6792dd3618043689e9",
      "snapshot": "knowledge/evidence/sources/sha256/168a7c81850500aa1d6f7153ff7481d81eabb3457305ca6792dd3618043689e9.md"
    },
    {
      "id": "SRC-ed754211fe9f301007ffce7b",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Release/Ratan Release Plan 2026/Ratan New Onboarding Checklist 2026/YYYY_MM_DD_CHG000000_CDS/page.md",
      "revision": "sha256:3ca2bbcdd1a736a849966afefcb06ff143553004e0a67abc8dc121b96fc69044",
      "sha256": "3ca2bbcdd1a736a849966afefcb06ff143553004e0a67abc8dc121b96fc69044",
      "snapshot": "knowledge/evidence/sources/sha256/3ca2bbcdd1a736a849966afefcb06ff143553004e0a67abc8dc121b96fc69044.md"
    },
    {
      "id": "SRC-f377dd5c3ee99af7752b2edf",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Release/Ratan Release Plan 2026/Ratan Pre-Cab Checklist 2026/2026_09_26_CHG1083456_Trade_Control_Bug_Fix/page.md",
      "revision": "sha256:9b6370d76aaf68228ddbc80306698a3b63f02567014f8aa05c39517c7e54b753",
      "sha256": "9b6370d76aaf68228ddbc80306698a3b63f02567014f8aa05c39517c7e54b753",
      "snapshot": "knowledge/evidence/sources/sha256/9b6370d76aaf68228ddbc80306698a3b63f02567014f8aa05c39517c7e54b753.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:20:50.474448+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "RATAN Trade Control expansion requests",
  "summary": "The June 2026 request scopes UK FXO trade tickets and contract validation, including netted trades.",
  "related": [],
  "open_questions": [
    "Who defines the effective C&A/Apollo error-code inventory, retry exhaustion behavior, and manual recovery ownership?",
    "Which rate source, precision/tolerance, cut timezone and validation authorization define the option-expiry exception and spot-ticket controls?",
    "Which scoped permission rule permits null-entity trades for GBS India while preserving other data-entitlement restrictions?"
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Automated checks do not establish complete writing review.",
    "Retained intent does not establish current approval, execution or rollout."
  ]
}
---
# RATAN Trade Control expansion requests

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

RATAN Trade Control expansion requests. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The June 2026 request scopes UK FXO trade tickets and contract validation, including netted trades.

## Documented knowledge

### FXO manual validation

The June 2026 request scopes UK FXO trade tickets and contract validation, including netted trades. It requests additional history columns, including netting history. Its real-time SCBML flow uses TDS3 upstream and Razor downstream. Exceptions and validation remain manual user work under the referenced Trade Control workflow; the selected source defines no additional ACK details.

[Source 57, lines 17-18](../../../../knowledge/evidence/sources/sha256/082cebade6e1a2ae48bcc07f09ae389d84bcfc2124f2622daf6626c4265d9f80.md#L17-L18) [Source 57, lines 31-32](../../../../knowledge/evidence/sources/sha256/082cebade6e1a2ae48bcc07f09ae389d84bcfc2124f2622daf6626c4265d9f80.md#L31-L32) [Source 57, lines 46-46](../../../../knowledge/evidence/sources/sha256/082cebade6e1a2ae48bcc07f09ae389d84bcfc2124f2622daf6626c4265d9f80.md#L46-L46)

### C&A and Falcon scope

The C&A request adds Sabre Native, BTS, BCSStella, APEX, Razor FX, Razor ALM, and Murex trade processing for PV and non-PV rules. Country and product scope is global/all. Sabre and Razor trade messages retain the TDS3-to-message-bridge path; Falcon integration uses a real-time API. It calls for exponential-backoff Falcon retries, three times, without manual intervention. Exception handling refers to 5xx and 4xx codes but explicitly leaves technical-exception decisions for user confirmation. Only certain error codes receive three automatic retries; business/data-quality issues alert Ops. This does not define the missing code inventory or recovery contract.

[Source 58, lines 16-18](../../../../knowledge/evidence/sources/sha256/0d5fe121b5bae684b2f7d1b356fd51d4d981db2d3984b853c66209afdd1aea32.md#L16-L18) [Source 58, lines 31-32](../../../../knowledge/evidence/sources/sha256/0d5fe121b5bae684b2f7d1b356fd51d4d981db2d3984b853c66209afdd1aea32.md#L31-L32) [Source 58, lines 47-47](../../../../knowledge/evidence/sources/sha256/0d5fe121b5bae684b2f7d1b356fd51d4d981db2d3984b853c66209afdd1aea32.md#L47-L47) [Source 58, lines 51-51](../../../../knowledge/evidence/sources/sha256/0d5fe121b5bae684b2f7d1b356fd51d4d981db2d3984b853c66209afdd1aea32.md#L51-L51)

### Option expiry rate controls

The September 2026 request calls for a cut-level blotter showing applied rates by currency pair. More than one rate for the same currency pair and cut must trigger an exception. Users can extract trade details for trades fixed within the cut, validate dashboard rates with corresponding validation of generated spot tickets, and refresh details. These five requested capabilities do not establish the rate source, numeric tolerance, exception ownership, or executed behavior.

[Source 68, lines 10-10](../../../../knowledge/evidence/sources/sha256/168a7c81850500aa1d6f7153ff7481d81eabb3457305ca6792dd3618043689e9.md#L10-L10)

### Detective-rule orchestration draft

The undated placeholder CDS checklist requests real-time RATAN-to-Apollo Rule Engine API integration for post-trade detective rules. Orchestration calls RATAN and Apollo foundation services. Scope is global and all products. It lists API request validation and three retries. Manual intervention, exception handling, and data-issue ownership remain TBD. It mentions 500 and 400 codes without a complete retry mapping. Placeholder dates and control fields provide no rollout or acceptance authority.

[Source 70, lines 16-18](../../../../knowledge/evidence/sources/sha256/3ca2bbcdd1a736a849966afefcb06ff143553004e0a67abc8dc121b96fc69044.md#L16-L18) [Source 70, lines 31-32](../../../../knowledge/evidence/sources/sha256/3ca2bbcdd1a736a849966afefcb06ff143553004e0a67abc8dc121b96fc69044.md#L31-L32) [Source 70, lines 46-47](../../../../knowledge/evidence/sources/sha256/3ca2bbcdd1a736a849966afefcb06ff143553004e0a67abc8dc121b96fc69044.md#L46-L47) [Source 70, lines 51-51](../../../../knowledge/evidence/sources/sha256/3ca2bbcdd1a736a849966afefcb06ff143553004e0a67abc8dc121b96fc69044.md#L51-L51)

### Null booking-entity display request

The September 2026 bug entry requests that the Exception blotter display trades with null booking entity for a GBS India user. This is a bounded requested correction. It does not grant unrestricted data access or define visibility for other users or countries.

[Source 72, lines 7-8](../../../../knowledge/evidence/sources/sha256/9b6370d76aaf68228ddbc80306698a3b63f02567014f8aa05c39517c7e54b753.md#L7-L8)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Who defines the effective C&A/Apollo error-code inventory, retry exhaustion behavior, and manual recovery ownership?
- Which rate source, precision/tolerance, cut timezone and validation authorization define the option-expiry exception and spot-ticket controls?
- Which scoped permission rule permits null-entity trades for GBS India while preserving other data-entitlement restrictions?
