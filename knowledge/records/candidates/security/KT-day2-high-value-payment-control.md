---
type: KnowledgeTopic
id: KT-day2-high-value-payment-control
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-36191270afaa98859699af7f
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/High Value Payment Control - RATAN/HVP
    Tech Design/page.md
  revision: sha256:455091d633e273eedee539a6a5cdd8f18c16c96038a79dc714954ed8d3936abc
  sha256: 455091d633e273eedee539a6a5cdd8f18c16c96038a79dc714954ed8d3936abc
- id: SRC-96adaf08b09241a7a8b35f1d
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/High Value Payment Control - RATAN/page.md
  revision: sha256:0e87eff30a2907b6d5341924c21c30752c1366c3a59e2ac2e5f0c721fd04e10e
  sha256: 0e87eff30a2907b6d5341924c21c30752c1366c3a59e2ac2e5f0c721fd04e10e
classification: security
scope: High-value payment authorization and outbound control intent
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- KT-settlement-multi-exception-control
open_questions:
- 'KDQ-2a2f8eb636: Which effective HVP profile limits, identity type, and complete
  lastUser update rules govern each action?'
- 'KDQ-523e26d357: Which approved header schema and service API version apply, and
  which FMRP affirmation-limit option is selected?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:44:20.733931+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# High-value payment authorization and outbound control intent

## Scope

High-value payment authorization and outbound control intent.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### HVP-01 — Scope, amount display, and approval limits

The high-value-payment requirement covers BCS, LOANIQ, and FMRP. Korea ENISIS remains excluded.
FMRP/LOANIQ expose USD-equivalent amounts in the blotter and permit filtering through existing mandatory query conditions.
BCS does not receive the proposed high-value exception, USD display, or threshold-filter enhancements.
BCS checker approvals use existing authorization-limit static. BCS single-level affirmation also requires an authorization-limit check.
FMRP affirmation retains two alternatives: remove the action or add the limit check.
The source retains failed-cashflow release and requires checker profile limits; its removal proposal is struck through.
The target FMO_OPS_BOS limit is below USD 500 million. Other retained limits are BOC below 30m, BO below 100m, BOL below 1bn, and BOM below 4bn.
A new BOSM profile is rejected in the source clarification. Current effective profile assignment remains unverified.

[Original evidence](../../../evidence/sources/sha256/0e87eff30a2907b6d5341924c21c30752c1366c3a59e2ac2e5f0c721fd04e10e.md#L3-L20). [Original evidence](../../../evidence/sources/sha256/0e87eff30a2907b6d5341924c21c30752c1366c3a59e2ac2e5f0c721fd04e10e.md#L24-L39). [Original evidence](../../../evidence/sources/sha256/0e87eff30a2907b6d5341924c21c30752c1366c3a59e2ac2e5f0c721fd04e10e.md#L117-L127).

### HVP-02 — STP flag and last-user contract

The intended `stpFlag` is Y for STP and N for NSTP. Every manual action except Add Comment makes the flow NSTP.
`lastUser` is blank for STP. Maker/checker actions supply the last checker PSID; single-level actions supply the maker PSID.
The detailed action matrices contain blank user cells. They do not establish a complete actor-update rule for every action.
A comment row marked Y does not prove that adding a comment resets an already NSTP flow to STP.
Automatic split children inherit STP/NSTP information from the parent.
Manual BCS net resultants with no attached user ID remain an unresolved case.
The source alternates FMID, PSID, and bank ID labels. Their identity mapping is not established here.

[Original evidence](../../../evidence/sources/sha256/0e87eff30a2907b6d5341924c21c30752c1366c3a59e2ac2e5f0c721fd04e10e.md#L24-L39). [Original evidence](../../../evidence/sources/sha256/0e87eff30a2907b6d5341924c21c30752c1366c3a59e2ac2e5f0c721fd04e10e.md#L41-L115). [Original evidence](../../../evidence/sources/sha256/0e87eff30a2907b6d5341924c21c30752c1366c3a59e2ac2e5f0c721fd04e10e.md#L117-L127).

### HVP-03 — Proposed service responsibilities

Orchestration extracts cashflow ID and business version, then obtains STP/NSTP and last-user information from Lifecycle.
It adds outbound message headers while routing LOANIQ toward Message Bridge and FMRP toward SWIFT Service.
Lifecycle supplies the internal lookup API. SWIFT Service receives those headers and adds MT/MX headers.
Query Service persists and queries USD-equivalent amounts.
The selected design ends at a Netting Service heading. It defines no netting-service responsibility in that range.

[Original evidence](../../../evidence/sources/sha256/455091d633e273eedee539a6a5cdd8f18c16c96038a79dc714954ed8d3936abc.md#L2-L26).

## Connections

Related canonical IDs: `KT-settlement-multi-exception-control`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
