---
type: KnowledgeTopic
id: KT-day2-auto-netting-service-design
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-728e9f456bbdc27bad60be7f
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Auto Netting Technical Design.md
  revision: sha256:57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102
  sha256: 57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102
- id: SRC-a87cb67c6cb8e24370092e4a
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Auto Netting Technical Design/page.md
  revision: sha256:57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102
  sha256: 57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102
- id: SRC-2f8174c6b82710efd3882562
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Auto Netting Technical Design.md
  revision: sha256:57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102
  sha256: 57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102
- id: SRC-96d49e9df333e28f36ce80d4
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Refactor Netting & Status Move Process.md
  revision: sha256:24f4d0930773aae8ab1320998becf5b575941e8a58677116b6c26e0c1e1c98e0
  sha256: 24f4d0930773aae8ab1320998becf5b575941e8a58677116b6c26e0c1e1c98e0
- id: SRC-56a609e0cd98dfe15e17fcc1
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Refactor Netting & Status Move Process/page.md
  revision: sha256:24f4d0930773aae8ab1320998becf5b575941e8a58677116b6c26e0c1e1c98e0
  sha256: 24f4d0930773aae8ab1320998becf5b575941e8a58677116b6c26e0c1e1c98e0
- id: SRC-66e20fc8b6ed049100ff590b
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Refactor Netting & Status Move Process.md
  revision: sha256:24f4d0930773aae8ab1320998becf5b575941e8a58677116b6c26e0c1e1c98e0
  sha256: 24f4d0930773aae8ab1320998becf5b575941e8a58677116b6c26e0c1e1c98e0
- id: SRC-b856e0bfc6b6ff7370ab832d
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Refactor Netting Process.md
  revision: sha256:cbd81e8c0f004b1932bf44c444bf679e0c75a75b0effc95676a7cafe149d541a
  sha256: cbd81e8c0f004b1932bf44c444bf679e0c75a75b0effc95676a7cafe149d541a
- id: SRC-a694d15c35f82d2ecb199b4b
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Refactor Netting Process/page.md
  revision: sha256:cbd81e8c0f004b1932bf44c444bf679e0c75a75b0effc95676a7cafe149d541a
  sha256: cbd81e8c0f004b1932bf44c444bf679e0c75a75b0effc95676a7cafe149d541a
- id: SRC-33fe500beb5368bae4a68aed
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/Refactor Netting Process.md
  revision: sha256:cbd81e8c0f004b1932bf44c444bf679e0c75a75b0effc95676a7cafe149d541a
  sha256: cbd81e8c0f004b1932bf44c444bf679e0c75a75b0effc95676a7cafe149d541a
- id: SRC-6d80375fb0abeea7286469d1
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/rule engine rule_action_event：.md
  revision: sha256:979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d
  sha256: 979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d
- id: SRC-bd2c1b624321a295d3e5c02b
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/rule engine rule_action_event：/page.md
  revision: sha256:979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d
  sha256: 979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d
- id: SRC-858ba0f0fa2d6afd923d6ff7
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Auto Netting/rule engine rule_action_event：.md
  revision: sha256:979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d
  sha256: 979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d
generated:
  by: agent:codex
  at: '2026-11-15T11:41:47Z'
verified: []
classification: architecture
scope: Proposed Cash Settlement auto-netting APIs, service boundaries, persistence, and rule lifecycle mappings.
summary: The technical drafts separate lifecycle status changes from netting operations and map rule-management events, states, and actions.
related:
- KT-settlement-auto-netting
- KT-day2-swap-agent
open_questions:
- Which owner approves the service boundary and API/schema contract?
- What is the approved ordering of status changes and resultant generation?
- Do blank action or rule_action cells represent no action, or are mappings missing?
---
# Auto-netting service design

## Scope

This candidate records proposed Day 2 service boundaries, APIs, and rule lifecycle mappings.

## Summary

The designs assign cashflow status changes to a lifecycle service and netting operations to a netting service.
They also map rule operations to event types, stored statuses, frontend actions, and rule actions.

## Documented knowledge

Rule metadata contains a UUID, execution date and time, STP level, netting type, and activation time.
[Rule metadata](../../../evidence/sources/sha256/57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102.md#L47-L58)

The design proposes a scheduled job endpoint and a rule-check endpoint.
The rule-check response distinguishes matched and unmatched rules.
[Job and rule-check APIs](../../../evidence/sources/sha256/57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102.md#L62-L120)

Two tables describe cashflow and rule configuration persistence.
They include rule identity, grouping, execution status, and resultant mappings.
[Persistence design](../../../evidence/sources/sha256/57531aed05a519cfba3274a57e4f89529e38abd2068f34737ebd37e5720b9102.md#L122-L157)

The refactor designs assign cashflow initialization and lifecycle status changes to the lifecycle service.
They assign net, unnet, rule checks, component status, and renet operations to the netting service.
[Service responsibilities](../../../evidence/sources/sha256/24f4d0930773aae8ab1320998becf5b575941e8a58677116b6c26e0c1e1c98e0.md#L81-L106) [Earlier responsibility design](../../../evidence/sources/sha256/cbd81e8c0f004b1932bf44c444bf679e0c75a75b0effc95676a7cafe149d541a.md#L88-L95)

The earlier refactor asks whether resultant generation should precede or follow status updates.
It also asks how to unnet a resultant.
[Refactor questions](../../../evidence/sources/sha256/cbd81e8c0f004b1932bf44c444bf679e0c75a75b0effc95676a7cafe149d541a.md#L139-L145)

The rule engine mapping lists these event, status, and action values for rule operations.
The blank entries below remain blank as shown in the source.
[Rule event mapping](../../../evidence/sources/sha256/979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d.md#L1-L13)

| Operation and user action | Event type | Rule status | Frontend action | Rule action |
| --- | --- | --- | --- | --- |
| Create: maker create | SAVE | ADD_PENDING | blank | blank |
| Create: checker approve | CONFIRM | LIVE | confirm | create_confirm |
| Create: checker reject | REMOVE | DEAD | reject | blank |
| Update: maker update old rule | CONFIRM (old) | LIVE | update | blank |
| Update: save new rule | SAVE (new) | UPDATE_PENDING | blank | blank |
| Update: checker approve old rule | REMOVE (old) | DEAD | blank | blank |
| Update: checker approve new rule | CONFIRM (new) | LIVE | confirm | update_confirm |
| Update: checker reject new rule | REMOVE (new) | DEAD | reject | blank |
| Enable | CONFIRM | LIVE | enable | enable |
| Disable | REMOVE | DISABLED | disable | disable |
| Delete | REMOVE | DEAD | null | null |

The two selected page identities for the event mapping have the same source hash.
Both identities remain declared because the imported collection contains both paths.
The other listed aliases also retain source identities for those same bytes.
They do not represent separate current selection reviews.
[First identity](../../../evidence/sources/sha256/979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d.md#L1-L13) [Byte-identical alias](../../../evidence/sources/sha256/979919a988ccd522420dc0b8d8fad9745f9b8fdd05960148b4620ccd71fee14d.md#L1-L13)

## Connections

The [auto-netting topic](../settlement/KT-settlement-auto-netting.md) describes rule selection and scheduled cashflow outcomes.
The [Swap Agent topic](../settlement/KT-day2-swap-agent.md) records payment-specific netting and suppression proposals.

## Evidence limits

These sources describe technical proposals.
The source owner, current approval, implementation, deployment, and execution were not inspected.
The mapping leaves several action cells blank without defining whether the values are intentionally absent.

## Open questions

Owner: unknown.

- Which owner approves the service boundary and API/schema contract?
- What is the approved ordering of status changes and resultant generation?
- Do blank action or rule_action cells represent no action, or are mappings missing?
