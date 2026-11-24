---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-amendment-reversal-rebook-exceptions",
  "version": 2,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-0158e2dc7d405c5a9379e540",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Ingenuine Rebook Exception in Ratan/page.md",
      "revision": "sha256:6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5",
      "sha256": "6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5",
      "snapshot": "knowledge/evidence/sources/sha256/6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5.md"
    },
    {
      "id": "SRC-82d0fde7244b6f0560ea6013",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Release/Ratan Release Plan 2026/Ratan Pre-Cab Checklist 2026/2026_05_23_CHG0974600_Ratan BAU Monthly Release - May/page.md",
      "revision": "sha256:5e99938658406f796bb1a486e0212b84e6701cf320a3ab0e512822d246de327a",
      "sha256": "5e99938658406f796bb1a486e0212b84e6701cf320a3ab0e512822d246de327a",
      "snapshot": "knowledge/evidence/sources/sha256/5e99938658406f796bb1a486e0212b84e6701cf320a3ab0e512822d246de327a.md"
    },
    {
      "id": "SRC-b92254f37d821df4383ad248",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/NDS Auto Netting.md",
      "revision": "sha256:1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d",
      "sha256": "1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d",
      "snapshot": "knowledge/evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md"
    },
    {
      "id": "SRC-fb926c5c667e80bbfae2d99f",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/NDS Auto Netting/page.md",
      "revision": "sha256:1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d",
      "sha256": "1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d",
      "snapshot": "knowledge/evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md"
    },
    {
      "id": "SRC-52ea4b749f13dcd53145646b",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Netting Function Flow/page.md",
      "revision": "sha256:639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708",
      "sha256": "639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708",
      "snapshot": "knowledge/evidence/sources/sha256/639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708.md"
    },
    {
      "id": "SRC-7cdd706104b50bf966b5d71e",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/IRS Fix Leg & Floating leg payment handling/page.md",
      "revision": "sha256:f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d",
      "sha256": "f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d",
      "snapshot": "knowledge/evidence/sources/sha256/f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d.md"
    },
    {
      "id": "SRC-b92254f37d821df4383ad248",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/NDS Auto Netting.md",
      "revision": "sha256:1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d",
      "sha256": "1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d",
      "snapshot": "knowledge/evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md"
    },
    {
      "id": "SRC-52ea4b749f13dcd53145646b",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Netting Function Flow/page.md",
      "revision": "sha256:639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708",
      "sha256": "639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708",
      "snapshot": "knowledge/evidence/sources/sha256/639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T00:54:23.316359+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Proposed reversal and rebook exception handling for amendments to released cashflows.",
  "summary": "The design pairs an original cashflow withdrawal with its replacement but says the current system lacks direct linkage to identify the pair reliably. A separate dictionary describes Reversal and Rebook reason values without defining pairing.",
  "related": [
    "KT-settlement-cashflow-identity-and-stella-write-back",
    "KT-settlement-cpn-netting",
    "KT-settlement-auto-netting",
    "KT-settlement-payment-amount-adjustment"
  ],
  "open_questions": [
    "Which source event and identifier bind a released cashflow withdrawal to the replacement cashflow for exception generation?",
    "Does the proposed direction filter or post-Uber trade event define the accepted implementation path?",
    "Does the 23 May 2026 pre-cab entry define an approved rebook rule, and which day calendar and boundary apply?",
    "Which dated entity and product scope governs the proposed NDS and IRS post-release exception variants?"
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Semantic review is bound separately to final draft bytes.",
    "Source/hash/range/citation checks do not establish complete ASD writing review.",
    "No current applicability, approval, implementation, execution or rollout established."
  ]
}
---
> **PROPOSED candidate:** Historical and proposed statements retain their source limits. Human publication review is pending.

# Released amendment reversal and rebook exceptions

## Scope

This candidate records proposed exception handling for an amendment after the original cashflow has been released from RATAN.

## Summary

The source proposes a reversal exception for the withdrawal of the released cashflow and a rebook exception for its replacement.
It also identifies a missing direct link between the two cashflows.

## Documented knowledge

The problem statement describes an amendment that withdraws the original cashflow and creates a new one.
For a released original, it calls for additional operations validation before release.
It proposes a reversal exception for the withdrawal and a rebook exception for the new cashflow.
[Amendment and exception requirement](../../../../knowledge/evidence/sources/sha256/6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5.md#L1-L13)

The source says the system lacks a direct link between the original and new cashflows.
It says the system therefore cannot reliably identify amendment-driven new cashflows for rebook exception generation.
It lists adding direction to the query criteria and considering a trade event after Uber is enabled as potential enhancements.
[Linkage gap and proposed enhancements](../../../../knowledge/evidence/sources/sha256/6db8ae4f3bb65b6166700b396cd47cedcb17d291b0f146863a97043bfb984ab5.md#L45-L48)

### Dated pre-cab rebook tagging entry

A 23 May 2026 pre-cab entry lists a rebook-exception tagging change from within 10 days to 5 days for the same trade ID. This is a dated release-scope statement. It does not define calendar versus business days, boundary handling, approval, or effective rollout. Do not treat five days as the current rule until its authority and applicability are confirmed. [Pre-cab rebook tagging entry](../../../../knowledge/evidence/sources/sha256/5e99938658406f796bb1a486e0212b84e6701cf320a3ab0e512822d246de327a.md#L19)

### Cashflow event-reason field

The dictionary describes `Cashflow.Cashflow_Event_Reason` as an indicator for a cashflow `Reversal` or `Rebook`. This entry does not specify how those cashflows are paired. [Cashflow event-reason dictionary field](../../../../knowledge/evidence/sources/sha256/639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708.md#L582)

### NDS post-release scope boundary

The NDS proposal distinguishes amendment and cancellation before versus after resultant release.
Before release, amendment auto-un-nets the resultant and auto-nets reversal/new in the next cycle.
Before-release cancellation auto-un-nets, cancels the original, and leaves the other component awaiting a later netting cycle.
If its partner never arrives, that component remains WAITING for manual investigation.
After release, amendment or re-fixing holds reversal and new as NSTP REVERSAL and REBOOK for manual handling.
After-release cancellation holds the component reversal; system and manual un-net are disallowed in this NDS scenario.
These controls are NDS-specific proposed intent, without current applicability or execution evidence.
[NDS event conditions](../../../../knowledge/evidence/sources/sha256/1092be71ca370ec5f35b86e18375c1305305197e53fe4f95543a5bd20363c03d.md#L12-L14)

### Separate IRS post-settlement example

The IRS example describes re-fixing after a resultant is settled.
It holds the floating-leg withdrawal and replacement in WAITING with “Cancel / Amend after payment release.”
Operations then manually net those two cashflows into a WAITING resultant.
This example does not establish a universal REVERSAL/REBOOK reason mapping or a pairing identity contract.
Its earlier VERIFIED resultant example does not supersede conflicting state descriptions in related sources.
[IRS post-settlement example](../../../../knowledge/evidence/sources/sha256/f24f6fc56692530ae5dc41c589df84cc3eabf90213d0761fe315f5308b22c69d.md#L133-L137)

## Connections

The [cashflow identity topic](../../../../knowledge/records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md) covers source IDs, versioning, and duplicate handling.
The [CPN netting topic](../../../../knowledge/records/candidates/settlement/KT-settlement-cpn-netting.md) describes separate released-resultant reversal scenarios.
The [auto-netting topic](../../../../knowledge/records/candidates/settlement/KT-settlement-auto-netting.md) covers rule-driven resultant handling.
The [payment adjustment topic](../../../../knowledge/records/candidates/settlement/KT-settlement-payment-amount-adjustment.md) records an unresolved question about downstream rebook linkage.

## Evidence limits

The primary source records a design proposal and a system limitation.
The pre-cab entry records a dated release-scope change, not an approved current rule.
The NDS and IRS examples do not establish their applicability to other products or approved current rule precedence.
The sources do not establish approval, implementation, deployment, or current behavior.
The field dictionary does not specify the identity contract or pairing rule.
The primary amendment source does not define a complete identity contract, qualifying event catalogue, or accountable owner.

## Open questions

Owner: unknown.

- Which source event and identifier bind a released cashflow withdrawal to the replacement cashflow for exception generation?
- Does the proposed direction filter or post-Uber trade event define the accepted implementation path?
- Does the 23 May 2026 pre-cab entry define an approved rebook rule, and which day calendar and boundary apply? [SRC-82d0fde7244b6f0560ea6013, original line 19]
- Which dated entity and product scope governs the proposed NDS and IRS post-release exception variants?
