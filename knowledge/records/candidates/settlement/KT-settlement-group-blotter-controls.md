---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-group-blotter-controls",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-298ca97600640b280c18fd96",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Group Blotter Enhancement/page.md",
      "revision": "sha256:6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7",
      "sha256": "6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7",
      "snapshot": "knowledge/evidence/sources/sha256/6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7.md",
      "original_ranges": [
        [
          1,
          3
        ],
        [
          9,
          12
        ],
        [
          14,
          18
        ],
        [
          21,
          27
        ]
      ]
    },
    {
      "id": "SRC-7b6c9bb2c361cd2f8de82e40",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/2025 changes/Bulk manual stp for Group Blotter/page.md",
      "revision": "sha256:8a2e628df693be7b7a4d9002f774ea2e0ea914cd684d7259cc61d1d596a428ed",
      "sha256": "8a2e628df693be7b7a4d9002f774ea2e0ea914cd684d7259cc61d1d596a428ed",
      "snapshot": "knowledge/evidence/sources/sha256/8a2e628df693be7b7a4d9002f774ea2e0ea914cd684d7259cc61d1d596a428ed.md",
      "original_ranges": [
        [
          3,
          13
        ]
      ]
    },
    {
      "id": "SRC-64f51b4a4489cdc47b76a18f",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/2026 Changes/Group Blotter Requirement/page.md",
      "revision": "sha256:fdaf4d1b4eb72faa09b995b380e5bc2755ebecdb22829a844c3a67df58a2efc9",
      "sha256": "fdaf4d1b4eb72faa09b995b380e5bc2755ebecdb22829a844c3a67df58a2efc9",
      "snapshot": "knowledge/evidence/sources/sha256/fdaf4d1b4eb72faa09b995b380e5bc2755ebecdb22829a844c3a67df58a2efc9.md",
      "original_ranges": [
        [
          3,
          18
        ]
      ]
    }
  ],
  "generated": {
    "by": "agent:codex",
    "at": "2026-11-15T09:08:26.917456+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Documented Group Blotter Manual STP selection, processing, and field projection.",
  "summary": "The business proposal and technical design specify different status predicates at different steps. The field list defines a separate cashflow and trade projection.",
  "related": [],
  "open_questions": [
    "How do PENDING_TRADE_VALIDATION, DATA_VALIDATION_FAILED, PENDING_PRE_GROUP, and PENDING_PREV_GROUP map between UI action eligibility, stored group status, and the closed decision by release?",
    "How does the bulk service use the original single-message logic after precheck, and what replay and mixed-result rules protect against duplicate payments?",
    "Which control takes precedence when the bulk UI permits a pending-validation row and the trade-validation design disables Manual STP?",
    "Which release activates the SCBML and Uber settlement-method and RFI portfolio projections?"
  ]
}
---
# Group Blotter controls

## Scope

This topic covers Group Blotter pagination, Manual STP, and the 2026 field list. It preserves the documented UI and processing predicates.

## Summary

Group Blotter gives operators a path to send selected cashflows to Cashflow Blotter. The business proposal and technical design use different status predicates. The field list defines a separate projection for cashflow and trade fields.

## Documented knowledge

### Action eligibility and warning

The Day 2 proposal loads 1,000 items by default. The operator can load the next 1,000 items or set the page size to 5,000. Its background describes Manual STP for a single cashflow as the existing path. The requirement notes PENDING or ERROR for that single action. [Background](../../../evidence/sources/sha256/6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7.md#L3) [Pagination and controls](../../../evidence/sources/sha256/6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7.md#L11-L12).

For multiple selected cashflows, the proposal exposes Manual STP when every selected cashflow belongs to a group in PENDING_TRADE_VALIDATION or PENDING_PRE_GROUP. It specifies an error when the selection includes another group status. Before processing, a warning tells operators to act only when the support team instructs them. It shows the selected cashflow count with the existing warning. [Action gate and warning](../../../evidence/sources/sha256/6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7.md#L12).

The 4 November 2025 closed entry adds a group status restriction in response to duplicate-payment risk. That entry uses PENDING_PREV_GROUP where the requirement text uses PENDING_PRE_GROUP. The selected material leaves their relationship open. The proposal references separate displays for all processed and all failed results. Details of those displays appear only in screenshots. [Closed risk decision](../../../evidence/sources/sha256/6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7.md#L18) [Result display references](../../../evidence/sources/sha256/6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7.md#L12).

### Processing and expected outcomes

The 2025 design applies its existing single-message logic when the message status is PENDING or ERROR. It requires that the previous major version have no pending group message. For multiple messages, it groups work by trade and uses multiple threads. Each trade goes through a precheck. On success, the design orders by major version and filters for DATA_VALIDATION_FAILED or PENDING_PRE_GROUP before it calls the original logic. On failure, it returns an error to the frontend. These are processing predicates. The design leaves their mapping to the UI action statuses open. [Single and bulk processing](../../../evidence/sources/sha256/8a2e628df693be7b7a4d9002f774ea2e0ea914cd684d7259cc61d1d596a428ed.md#L5-L13).

The Day 2 first scenario selects all cashflows in one PENDING_TRADE_VALIDATION group. It expects the cashflows to reach END, the group to reach COMPLETED, and the booking system event to be ManualDeliver. The second scenario selects a later PENDING_PRE_GROUP group while an earlier group for the same trade lacks an expected cashflow. It expects an error. The third scenario selects both fully received groups for the trade, one in PENDING_TRADE_VALIDATION and one in PENDING_PRE_GROUP. It expects END, COMPLETED, and ManualDeliver. [Expected business cases](../../../evidence/sources/sha256/6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7.md#L25-L27).

The business cases show cashflows in PENDING under a group with a separately named status. One eligible group can produce several selected cashflows. The second case shows that the UI gate alone does not guarantee success. [Selection and group outcomes](../../../evidence/sources/sha256/6bcb2e54cc2804f73a76d025beb0c52cf0bc7ed56824209974602fa0f2585bb7.md#L25-L27).

### Field projection

The 2026 list names these cashflow economic fields: booking entity SCI FMID, counterparty SCI FMID, pay or receive indicator, payment amount, payment currency, payment date, settlement method, and booking entity trade portfolio. It lists trade `LIEN_Monitoring` as economic. It lists trade `Contract_Typology`, `Linked_Package_Id`, and `Swap_Agent_Id` as special. [Cashflow fields](../../../evidence/sources/sha256/fdaf4d1b4eb72faa09b995b380e5bc2755ebecdb22829a844c3a67df58a2efc9.md#L7-L14) [Trade fields](../../../evidence/sources/sha256/fdaf4d1b4eb72faa09b995b380e5bc2755ebecdb22829a844c3a67df58a2efc9.md#L15-L18).

The settlement-method row uses the cashflow record in both paths. It labels SCBML as in production and links the Uber version to the Uber release. The portfolio row links its release to RFI. These release labels describe the source's stated scope. The list leaves filtering, grouping keys, and action eligibility unspecified. [Release qualifications](../../../evidence/sources/sha256/fdaf4d1b4eb72faa09b995b380e5bc2755ebecdb22829a844c3a67df58a2efc9.md#L13-L14).

## Connections

Group Blotter selection sits between upstream grouping and downstream cashflow processing. Trade completeness and prior-version ordering affect the documented action outcome. Grouping, monitoring, and trade validation retain their own source and claim scope.

## Evidence limits

The selected pages describe proposals and scenario expectations. The applicable release, source authority, and precise mapping between UI and processing statuses need confirmation. Screenshot content, partial success behavior, retry handling, and production behavior were not verified.

## Open questions

- How do PENDING_TRADE_VALIDATION, DATA_VALIDATION_FAILED, PENDING_PRE_GROUP, and PENDING_PREV_GROUP map between UI action eligibility, stored group status, and the closed decision by release?
- How does the bulk service use the original single-message logic after precheck, and what replay and mixed-result rules protect against duplicate payments?
- Which control takes precedence when the bulk UI permits a pending-validation row and the trade-validation design disables Manual STP?
- Which release activates the SCBML and Uber settlement-method and RFI portfolio projections?
