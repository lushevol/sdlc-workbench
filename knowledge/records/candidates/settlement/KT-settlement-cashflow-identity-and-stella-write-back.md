---
type: KnowledgeTopic
id: KT-settlement-cashflow-identity-and-stella-write-back
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-2309999b1527dff6b86fd17a
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/FX Cashflow Status Write Back
    - Razor to Stella/page.md
  revision: sha256:1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d
  sha256: 1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d
- id: SRC-c73dbcca86e954b7f4610e73
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/LifeCycle/Cashflow & Payment
    cashflow id management/page.md
  revision: sha256:2f5d809b7453b3284e626c71d9e9b68779e1d9eea1c826c4ed3be582a1fd170f
  sha256: 2f5d809b7453b3284e626c71d9e9b68779e1d9eea1c826c4ed3be582a1fd170f
- id: SRC-9b91aab0adadaa6d3755f23e
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/SUSPENDED vs PROJECTED cashflow
    status in Ratan/page.md
  revision: sha256:eb4192cfb68c5b57854823fba7f0cb0b632a4c79d6cb78c9dcc4f00edec575d9
  sha256: eb4192cfb68c5b57854823fba7f0cb0b632a4c79d6cb78c9dcc4f00edec575d9
- id: SRC-14e693609134a6475b41db72
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Surrounding System Integration/Ratan
    & Stella cashflow integration/page.md
  revision: sha256:0fc2d3d755dc6e3749bb531bb8a9f8bb13e4787feb609f0d790d6b8dea3d116f
  sha256: 0fc2d3d755dc6e3749bb531bb8a9f8bb13e4787feb609f0d790d6b8dea3d116f
- id: SRC-a56976b24a3831d085804c04
  resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/Function_RATAN-Settlement  0.0_Uber Validation+Payment Identify/page.md
  revision: sha256:da608afa9a303872a78de2a2ee327b9f724c3e8e8c6308aee7882fda7991f0a5
  sha256: da608afa9a303872a78de2a2ee327b9f724c3e8e8c6308aee7882fda7991f0a5
- id: SRC-ba77d2c98ededd97c6c19d2c
  resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and SABRE (FMRP STELLA)-29126/page.md
  revision: sha256:06cc17867a3296f811b4005254101c74dcdd1a03aa8a3829b72ad4c9e06cfeaf
  sha256: 06cc17867a3296f811b4005254101c74dcdd1a03aa8a3829b72ad4c9e06cfeaf
generated:
  by: agent:codex
  at: '2026-11-13T14:41:24.727146+00:00'
verified: []
classification: settlement
scope: Cash Settlement identity rules, FX status write-back through RATAN, and the proposed Stella lifecycle boundary.
summary: The identity design defines source and resultant IDs. The FX status write-back design aims to reduce duplicate payments.
  Acknowledgement and applicable version rules need confirmation.
related:
- KT-settlement-auto-netting
open_questions:
- Which flows, entities, and dates govern the Stella lifecycle and FX write-back rules?
- Which version and event fields define duplicate handling at each interface?
- Which Razor status, message ID, matching tolerance, and reversal conditions govern write-back?
- Who sends each ACK or NACK, and which reconciliation and recovery actions apply?
---
# Cashflow identity and Stella status write-back

## Scope

This draft covers Cash Settlement identity rules, FX status write-back through RATAN, and the proposed Stella lifecycle boundary.

## Summary

The identity design defines how RATAN represents source cashflows and allocates resultant cashflow IDs.
The FX write-back design uses Stella status updates to reduce duplicate payment risk.
The acknowledgement contract and the applicability of the dated proposals remain open.

## Documented knowledge

### Identity and duplicate handling

The identity design retains Stella's 12-character ID. It pads Murex 2.11 and the MxCash/Razor entry to 12 characters. It uses an M or R prefix respectively and adds zeros before the source ID. The design gives netting and split resultants new IDs unique across RATAN services and processes. The formats use N or S followed by 11 digits. The ID generator must handle concurrent requests. [Cashflow ID design](../../../evidence/sources/sha256/2f5d809b7453b3284e626c71d9e9b68779e1d9eea1c826c4ed3be582a1fd170f.md#L3-L7) [Resultant identity](../../../evidence/sources/sha256/2f5d809b7453b3284e626c71d9e9b68779e1d9eea1c826c4ed3be582a1fd170f.md#L16-L27)

The Uber validation description checks whether each cashflow was processed using cashflow ID and version. The Stella integration proposal lists cashflow ID, business version, and status update event for duplicate filtering. The Uber description leaves the version field unspecified. [Uber validation](../../../evidence/sources/sha256/da608afa9a303872a78de2a2ee327b9f724c3e8e8c6308aee7882fda7991f0a5.md#L9-L15) [Stella integration proposal](../../../evidence/sources/sha256/0fc2d3d755dc6e3749bb531bb8a9f8bb13e4787feb609f0d790d6b8dea3d116f.md#L7-L12)

### FX status write-back

The FX requirement routes Razor cashflow status through RATAN to Stella to reduce duplicate payment risk. It calls for SUSPENDED-MATURED on the matched Stella cashflow after Razor nets, splits, settles, or releases the cashflow. It does not require write-back for netting or split resultants, or for un-net or un-split events. It prefers to suppress repeat SUSPENDED-MATURED updates. [FX objective and scope](../../../evidence/sources/sha256/1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d.md#L3-L19)

Razor supplies no trade version under the stated assumption. RATAN matches to the latest Stella cashflow. The design compares booking entity, counterparty, currency, amount, value date, and pay or receive direction. The requirement also names a message ID. Currency conversion and amount rounding prompted proposed matching tolerances. Confirm how the message ID and tolerances enter the match. [Requirement linkage](../../../evidence/sources/sha256/1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d.md#L13-L19) [Match fields](../../../evidence/sources/sha256/1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d.md#L79-L94) [Tolerance assumptions](../../../evidence/sources/sha256/1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d.md#L51-L57)

For new cashflows and economic amendments, RATAN waits for the Razor cashflow. For non-economic amendments, the design carries SUSPENDED-MATURED forward when the previous Stella cashflow has that status. Its technical flow includes CCPNetted, restricts reversal status to None or Correction, and skips a Razor cashflow ID that was already processed successfully. Confirm the applicable trigger set. [Amendment and status flow](../../../evidence/sources/sha256/1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d.md#L63-L90)

### Stella lifecycle and acknowledgement

The China onboarding proposal assigns cashflow generation to Stella and lifecycle handling to post-trade processing. Stella owns business and cashflow versions in the proposal. RATAN advances its minor version for internal actions and resets it when Stella supplies a new business version. The proposal sends Released and Settled back to Stella and allows only Middle Office to amend such trades. Its amendment example requires withdrawal before replacement. [Proposed ownership and hard block](../../../evidence/sources/sha256/0fc2d3d755dc6e3749bb531bb8a9f8bb13e4787feb609f0d790d6b8dea3d116f.md#L3-L12) [Proposed version rules](../../../evidence/sources/sha256/0fc2d3d755dc6e3749bb531bb8a9f8bb13e4787feb609f0d790d6b8dea3d116f.md#L16-L20) [Amendment order](../../../evidence/sources/sha256/0fc2d3d755dc6e3749bb531bb8a9f8bb13e4787feb609f0d790d6b8dea3d116f.md#L63-L66)

A separate design discussion distinguishes suspension in Stella from suppression in RATAN. It describes a future policy to publish all FX cashflows as PROJECTED and calls for maker-checker control on manual straight-through processing of suspended cashflows. Confirm where these rules apply before combining them with the FX write-back design. [Suspension and suppression](../../../evidence/sources/sha256/eb4192cfb68c5b57854823fba7f0cb0b632a4c79d6cb78c9dcc4f00edec575d9.md#L3-L22) [Manual processing](../../../evidence/sources/sha256/eb4192cfb68c5b57854823fba7f0cb0b632a4c79d6cb78c9dcc4f00edec575d9.md#L38-L41)

The FX assumption says write-back has no ACK/NACK or reconciliation. The technical flow stores an internal NACK for an unmatched cashflow in phase 1. The FX interface section also says Razor must supply an ACK. The SABRE interface page describes a separate Stella ACK or NACK for booking events from RATAN. These statements name different parties or steps. The applicable acknowledgement and recovery rules require confirmation. [FX assumption](../../../evidence/sources/sha256/1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d.md#L49) [FX design](../../../evidence/sources/sha256/1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d.md#L84-L99) [SABRE booking response](../../../evidence/sources/sha256/06cc17867a3296f811b4005254101c74dcdd1a03aa8a3829b72ad4c9e06cfeaf.md#L9-L15)

## Connections

The auto-netting topic covers rule selection and netting outcomes. The identity design above covers how a resultant receives its ID. [Cash Settlement auto-netting](KT-settlement-auto-netting.md)

## Evidence limits

The FX source lists a 2024 target. The Stella proposal uses 2022 examples. The SABRE interface page records a March 2026 review and leaves its publication status blank. Effective scope and production behavior are unverified. [FX target](../../../evidence/sources/sha256/1f9c1d8fddee5e98f9e4649613648c1cd3a1a079349a84b2e4e8b31de68ccc9d.md#L7-L9) [Stella example](../../../evidence/sources/sha256/0fc2d3d755dc6e3749bb531bb8a9f8bb13e4787feb609f0d790d6b8dea3d116f.md#L56-L64) [SABRE review row](../../../evidence/sources/sha256/06cc17867a3296f811b4005254101c74dcdd1a03aa8a3829b72ad4c9e06cfeaf.md#L3-L7)

## Open questions

- Which flows, entities, and dates govern the Stella lifecycle and FX write-back rules?
- Which version and event fields define duplicate handling at each interface?
- Which Razor status, message ID, matching tolerance, and reversal conditions govern write-back?
- Who sends each ACK or NACK, and which reconciliation and recovery actions apply?
