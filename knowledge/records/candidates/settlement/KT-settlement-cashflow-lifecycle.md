---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-cashflow-lifecycle",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-f541d8b0b633f12efd37d44b",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Cashflow Logical Model & Templates/Cashflow Logical Model Fields & Data Store/page.md",
      "revision": "sha256:6f7aeec8ec18b42072f1e3243d5845539500d1ac69075f98a08c37c95e982064",
      "sha256": "6f7aeec8ec18b42072f1e3243d5845539500d1ac69075f98a08c37c95e982064",
      "snapshot": "knowledge/evidence/sources/sha256/6f7aeec8ec18b42072f1e3243d5845539500d1ac69075f98a08c37c95e982064.md"
    },
    {
      "id": "SRC-e03b4e34c339a47bb289884c",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Cashflow Logical Model & Templates/SCBML Template/page.md",
      "revision": "sha256:ca099b19c6f96a4d27fb195c106257aff3af258543c07796e2cb003d5d0823dc",
      "sha256": "ca099b19c6f96a4d27fb195c106257aff3af258543c07796e2cb003d5d0823dc",
      "snapshot": "knowledge/evidence/sources/sha256/ca099b19c6f96a4d27fb195c106257aff3af258543c07796e2cb003d5d0823dc.md"
    },
    {
      "id": "SRC-113036f16c331f1c8296ba71",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Cashflow Swift Suppression/page.md",
      "revision": "sha256:411359b9dd50ccbbbc55a0f6cede4bbf10a080fb74b1ed07fc733f82b074780e",
      "sha256": "411359b9dd50ccbbbc55a0f6cede4bbf10a080fb74b1ed07fc733f82b074780e",
      "snapshot": "knowledge/evidence/sources/sha256/411359b9dd50ccbbbc55a0f6cede4bbf10a080fb74b1ed07fc733f82b074780e.md"
    },
    {
      "id": "SRC-57d75465860a6b9ff5d01e47",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/LifeCycle/Status Machine/page.md",
      "revision": "sha256:066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b",
      "sha256": "066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b",
      "snapshot": "knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_finish_lane2",
    "at": "2026-11-16T02:08:19.414813+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Documented cashflow states, transitions, version dimensions, suppression, and common SCBML generation responsibilities.",
  "summary": "Track cashflow processing through state and version changes while preserving conflicting transition proposals.",
  "related": [
    "KT-settlement-cashflow-identity-and-stella-write-back",
    "KT-settlement-event-sequencing",
    "KT-settlement-hold-unhold",
    "KT-settlement-failed-cashflow-recovery",
    "KT-settlement-fx-utilization"
  ],
  "open_questions": [
    "Which state spelling and transition-matrix revision are authoritative?",
    "How do HOLD amendment, UnSplit, and suppressed-state Fail rows reconcile with dedicated designs?",
    "Are NOSTRO_MATCHED transition rows active despite the not-in-scope dictionary label?",
    "Which version reset and repeated-event rules govern each external producer?"
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
# Cashflow lifecycle and versions

## Scope

Documented cashflow states, selected transitions, version dimensions, and internal/external request contracts.
These isolated proposals require canonical integration and authority review.

## Summary

Track cashflow processing through state and version changes while preserving conflicting transition proposals.
These documents describe intended responsibilities and proposals. They do not establish current implementation or deployment.

## Documented knowledge

### WF-CF-035

The status design distinguishes projected, queued, waiting, hold, ready, released, settled, suppression, netting, failure, utilization, pastdue, and split states.

Exceptions: NOSTRO MATCHED is explicitly not in scope for now.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 3–31](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L3-L31)

Limit: Dictionary spelling differs from transition rows, including PARTIALLY-UTILIZED versus PARTIALLY_UTILIZED.

### WF-CF-036

New and Amendment initialize PROJECTED, NetNew/SplitNew initialize QUEUED, and materialization changes PROJECTED to QUEUED.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 35–48](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L35-L48)

Limit: No implementation, deployment, or business execution established.

### WF-CF-037

QUEUED evaluation routes netting or exception cases to WAITING, clean validation to READY, and suppression to its dedicated suppression state.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 49–75](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L49-L75)

Limit: No implementation, deployment, or business execution established.

### WF-CF-038

WAITING exception submit moves from Pending Operator to Pending Verification; checker rejection returns to operator, and approval clears exceptions into READY.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 76–90](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L76-L90)

Limit: No implementation, deployment, or business execution established.

### WF-CF-039

WAITING net/split, technical failure, hold, amendment, withdrawal, fail, and suppression have separate action transitions; READY supports release, direct settlement, pending acknowledgement, or reevaluation.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 91–203](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L91-L203)

Limit: Repeated rows and NA targets must not be collapsed into new rules.

### WF-CF-040

The matrix models manual settlement as RELEASED to pending verification, followed by checker approval to SETTLED or rejection to RELEASED.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 204–215](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L204-L215)

Limit: No implementation, deployment, or business execution established.

### WF-CF-041

The matrix sends HOLD Amendment to QUEUED, permits UnSplit from HOLD, and permits Fail from suppressed states, conflicting with dedicated hold and failure descriptions.

Source status: unresolved cross-document transition conflict.
[Retained original, lines 216–222](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L216-L222) [Retained original, lines 258–272](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L258-L272) [Retained original, lines 294–301](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L294-L301)

Limit: Do not infer that these rows are effective merely because they appear in a matrix.

### WF-CF-042

Netting components retain NETTED while their release/settle sub-status advances; resultant un-net becomes DEAD while component un-net becomes QUEUED.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 25–26](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L25-L26) [Retained original, lines 242–257](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L242-L257)

Limit: No implementation, deployment, or business execution established.

### WF-CF-043

Utilization transitions distinguish full/partial use, reversal, pastdue, and withdrawal; withdrawal on utilized amounts routes to ERROR, while PASTDUE withdrawal cancels.

Exceptions: Crossed-out PartialUtilize/PartialReverse rows do not establish active transitions.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 273–293](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L273-L293)

Limit: No implementation, deployment, or business execution established.

### WF-CF-044

The design distinguishes business version, cashflow version, and minor version; external requests update all three, while internal requests use minor version without business/cashflow version changes.

Conditions: External requests accept PROJECTED with New/Amendment/Withdrawal, or RELEASED/SETTLED/NETTED with Withdrawal or Withdrawal and New.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 307–316](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L307-L316)

Limit: This source does not explicitly state the minor-version reset rule present in the existing Stella identity candidate.

### Multiple payment selection

Only the payment marked isIntentToSettle true represents the settlement payment in a multi-payment cashflow.
The explicit fallback says to take the first payment when zero or more than one payment is marked true.
Exactly one true payment removes false-marked payments; single-payment input skips the check.
This fallback is a documented source rule, without proven safe ordering or owner acceptance for malformed flags.
The same source describes trade-ID plus trade-version lookup for parent data, but the selected field inventory is absent.
No unspecified trade fields or producer guarantees are inferred.
[Multi-payment selector](../../../../knowledge/evidence/sources/sha256/6f7aeec8ec18b42072f1e3243d5845539500d1ac69075f98a08c37c95e982064.md#L16-L29)
[Parent lookup scope](../../../../knowledge/evidence/sources/sha256/6f7aeec8ec18b42072f1e3243d5845539500d1ac69075f98a08c37c95e982064.md#L212-L216)

### Suppression purpose and reversal boundaries

Cashflow suppression means neither payment nor settlement accounting is required.
Payment/Swift suppression means payment is not required; accounting remains separate.
Incorrect client rules must be removed from their respective rule tables.
Automatic rule application is single-level; rule creation/deletion still requires maker/checker.
Manual suppression and undo require maker/checker.
Undo is permitted through value date, not beyond it.
After value date, the source routes required payment/accounting to Oscar, or payment-only handling to AMH/Oscar.
Amendment/cancellation starts a new lifecycle version.
[Suppression purposes](../../../../knowledge/evidence/sources/sha256/411359b9dd50ccbbbc55a0f6cede4bbf10a080fb74b1ed07fc733f82b074780e.md#L3-L6)
[Rule controls](../../../../knowledge/evidence/sources/sha256/411359b9dd50ccbbbc55a0f6cede4bbf10a080fb74b1ed07fc733f82b074780e.md#L8-L12)

The manual matrices accept PROJECTED or READY with NA substates, or WAITING outside the four suppression/undo types.
Maker initiation enters WAITING/PendingVerification with the matching suppression type.
Checker approval enters CASHFLOW SUPPRESSED or SWIFT SUPPRESSED; rejection rolls back the source status/substates.
Undo from either final suppressed state enters matching WAITING/PendingVerification.
Undo approval returns QUEUED with NA substates; rejection restores the original suppressed state.
The generic status matrix instead records NA rejection targets, leaving rollback interpretation unresolved.
[Suppression and undo matrices](../../../../knowledge/evidence/sources/sha256/411359b9dd50ccbbbc55a0f6cede4bbf10a080fb74b1ed07fc733f82b074780e.md#L18-L21)
[Generic rejection targets](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L174-L181)

The historical Razor flow sends SWIFT SUPPRESSED cashflows by value-date EOD for accounting only.
Post-EOD cancellation generates reversal, and amendment reversal plus new accounting.
This is dated source-specific intent; it does not supersede the separate RATAN accounting contract.
[Historical accounting boundary](../../../../knowledge/evidence/sources/sha256/411359b9dd50ccbbbc55a0f6cede4bbf10a080fb74b1ed07fc733f82b074780e.md#L23-L28)

### Important state-specific differences

READY with PendingAck handles withdrawal through QUEUED; READY without PendingAck cancels withdrawal directly.
RELEASED, SETTLED and NETTED withdrawals return QUEUED in their listed rows.
FAILED permits reinstatement, accounting acknowledgement and amendment/withdrawal transitions in this matrix.
The dictionary marks NOSTRO MATCHED outside scope even though transition rows include it.
Do not treat listed technical transitions as GUI permission grants.
UTILIZED and PARTIALLY_UTILIZED withdrawals become ERROR; PASTDUE withdrawal becomes CANCELLED.
Full reversal returns READY, while partial reversal of UTILIZED returns PARTIALLY_UTILIZED.
Crossed-out partial-use/reversal and SPLIT rows remain excluded from active conclusions.
UnSplit moves parent SPLIT to QUEUED and eligible child states to DEAD in this matrix.
Dedicated split requirements later describe parent WAITING plus exception; that precedence is unresolved.
[READY and released transitions](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L182-L215)
[Failed and netted transitions](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L236-L257)
[Utilization and unsplit transitions](../../../../knowledge/evidence/sources/sha256/066d2ca7cf2843d346875d6cb572c8b44adf21ffc5399dee1e4384af9621862b.md#L273-L301)

### Common SCBML generation responsibility

The template proposal defines common New, Amendment, and Withdrawal cashflow SCBML for domain services.
Netting calculates resultant values and generates the resultant SCBML through the predefined template.
The Murex interface maps inbound MxML values into the corresponding cashflow SCBML.
Domain services calculate bean values. Shared utility tools generate SCBML from the Java object.
The selected source excludes the field inventory and template body. Their schemas remain unconfirmed.
[Common template responsibilities](../../../../knowledge/evidence/sources/sha256/ca099b19c6f96a4d27fb195c106257aff3af258543c07796e2cb003d5d0823dc.md#L2-L9)

The logical-model design stores converted inbound Stella/Murex SCBML and workflow-generated cashflow results locally.
This describes intended persistence responsibilities without establishing deployed storage behavior.
[Persistence scope](../../../../knowledge/evidence/sources/sha256/6f7aeec8ec18b42072f1e3243d5845539500d1ac69075f98a08c37c95e982064.md#L1-L4)

## Connections

Related proposed or existing records: `KT-settlement-cashflow-identity-and-stella-write-back`, `KT-settlement-event-sequencing`, `KT-settlement-hold-unhold`, `KT-settlement-failed-cashflow-recovery`, `KT-settlement-fx-utilization`.

## Evidence limits

Claims use the selected original ranges. Adjacent original headings were inspected for context.
Linked diagrams, attachments, policies, configurations, and external destinations were not inspected.
Documented designs do not establish executed behavior or current rollout.
Source authority and current applicability remain unconfirmed.
No publication approval or business verification is recorded.

## Open questions

Owner: unknown.

- Which state spelling and transition-matrix revision are authoritative?
- How do HOLD amendment, UnSplit, and suppressed-state Fail rows reconcile with dedicated designs?
- Are NOSTRO_MATCHED transition rows active despite the not-in-scope dictionary label?
- Which version reset and repeated-event rules govern each external producer?
