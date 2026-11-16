---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-static-maker-checker-controls",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-0a283e023f601a7925c74a0a",
      "resource": "source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/BIC Netting Static.md",
      "revision": "sha256:16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8",
      "sha256": "16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8",
      "snapshot": "knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md"
    },
    {
      "id": "SRC-c4509b939f9d7a64a8cfc3d8",
      "resource": "source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/Netting and Nostro Static.md",
      "revision": "sha256:83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375",
      "sha256": "83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375",
      "snapshot": "knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md"
    },
    {
      "id": "SRC-f8a91aa1ae50a188cd333b83",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/BIC Netting Static/page.md",
      "revision": "sha256:16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8",
      "sha256": "16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8",
      "snapshot": "knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md"
    },
    {
      "id": "SRC-bbc41c132d0678876db3412a",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/BIC Netting Static.md",
      "revision": "sha256:16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8",
      "sha256": "16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8",
      "snapshot": "knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md"
    },
    {
      "id": "SRC-d7a5652466fb281990255496",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/Netting and Nostro Static/page.md",
      "revision": "sha256:83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375",
      "sha256": "83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375",
      "snapshot": "knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md"
    },
    {
      "id": "SRC-917c954ef25e83205850f91f",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/Netting and Nostro Static.md",
      "revision": "sha256:83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375",
      "sha256": "83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375",
      "snapshot": "knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:31:00.545853+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "BIC and netting static control intent",
  "summary": "The BIC tile permits `FMO_STA_CKR` and `FMO_STA_MKR` maintenance.",
  "related": [],
  "open_questions": [
    "Confirm current static profiles and lifecycle authority.",
    "Resolve the automatic-rule update contradiction for Pending Auto Netting refresh."
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
# BIC and netting static control intent

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

BIC and netting static control intent. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The BIC tile permits `FMO_STA_CKR` and `FMO_STA_MKR` maintenance.

## Documented knowledge

### BIC static lifecycle

The BIC tile permits `FMO_STA_CKR` and `FMO_STA_MKR` maintenance. Avoid leading and trailing spaces. Makers update records and delete `SAVE_CONFIRMED` records. Checkers approve or reject updates. Bulk delete applies to `SAVE_CONFIRMED` records. Bulk checker approval or rejection follows detail verification. `ADD_PENDING`, `UPDATE_PENDING`, and `DELETE_PENDING` record maker actions. `SAVE_CONFIRMED` makes approved additions or updates effective. Rejected updates preserve the original version. Approved deletion becomes `DELETE_CONFIRMED`, visible only in audit. Rejected additions become ineffective `DISCARDED` records.

[Source 29, lines 3-5](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L3-L5) [Source 29, lines 9-11](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L9-L11) [Source 29, lines 15-19](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L15-L19) [Source 29, lines 25-25](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L25-L25) [Source 29, lines 31-33](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L31-L33) [Source 29, lines 37-37](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L37-L37) [Source 29, lines 43-45](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L43-L45) [Source 29, lines 49-51](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L49-L51) [Source 29, lines 55-55](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L55-L55) [Source 29, lines 59-68](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L59-L68) [Source 30, lines 3-5](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L3-L5) [Source 30, lines 9-11](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L9-L11) [Source 30, lines 15-19](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L15-L19) [Source 30, lines 25-25](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L25-L25) [Source 30, lines 31-33](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L31-L33) [Source 30, lines 37-37](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L37-L37) [Source 30, lines 43-45](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L43-L45) [Source 30, lines 49-51](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L49-L51) [Source 30, lines 55-55](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L55-L55) [Source 30, lines 59-68](../../../../knowledge/evidence/sources/sha256/16eb218eb7fa00dcc2177a16d55cc9fd909ca25ee01a3724ecf719ee23d2dbc8.md#L59-L68)

### Netting rule creation

The netting and Nostro static tile uses the same two profiles. Netting rule types distinguish manual and automatic netting. Maker-selected fields form AND conditions, with a reason. Automatic rules add netting date/time, resultant STP level, and netting type. Listed STP levels are `NSTP_MAKER_CHECKER` and `NSTP_CHECKER_ONLY`. New rules become effective after checker approval. Maker and checker must differ.

[Source 33, lines 10-12](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L10-L12) [Source 33, lines 16-18](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L16-L18) [Source 33, lines 22-22](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L22-L22) [Source 33, lines 26-26](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L26-L26) [Source 33, lines 30-39](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L30-L39) [Source 34, lines 10-12](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L10-L12) [Source 34, lines 16-18](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L16-L18) [Source 34, lines 22-22](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L22-L22) [Source 34, lines 26-26](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L26-L26) [Source 34, lines 30-39](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L30-L39)

### Automatic-rule refresh boundaries

Creation refreshes matching cashflows with blank or null netting ID: WAITING Pending Netting/Pending Exception, or READY with null state type. It excludes WAITING Pending Another Leg/Pending Auto Netting, READY Pending Ack, HOLD, SUPPRESSED, NETTED, RELEASED, and SETTLED. Disabling refreshes only WAITING Pending Auto Netting cashflows tagged to that rule. Updating an automatic rule lists both tagged Pending Auto Netting cashflows and newly eligible matches. That update passage also excludes Pending Auto Netting, creating an unresolved contradiction. Manual-to-automatic changes use creation eligibility. Automatic-to-manual changes refresh tagged WAITING Pending Auto Netting cashflows. Preserve those operation-specific rules; do not broaden refresh to released or settled cashflows.

[Source 33, lines 36-36](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L36-L36) [Source 34, lines 36-36](../../../../knowledge/evidence/sources/sha256/83f5b2eef84f34815286027f8f7e570fb4c14dce2c4ba8578da604e6d09b9375.md#L36-L36)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm current static profiles and lifecycle authority.
- Resolve the automatic-rule update contradiction for Pending Auto Netting refresh.
