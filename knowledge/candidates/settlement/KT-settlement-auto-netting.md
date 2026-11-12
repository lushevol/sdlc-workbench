---
type: KnowledgeTopic
id: KT-settlement-auto-netting
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Netting/Netting
    Function Flow/page.md
  revision: sha256:639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708
  sha256: 639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708
- resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Netting/Netting
    Function Flow/attachments/netting-function-flow-page-source-v20260911.md
  revision: sha256:c98ed22769a19102e766f3dbdff3aa41ee52eef7426bef708f083a166b79d396
  sha256: c98ed22769a19102e766f3dbdff3aa41ee52eef7426bef708f083a166b79d396
- resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Settlement
    Day2 Requirement/Cashflow Auto Netting.md
  revision: sha256:a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62
  sha256: a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62
- resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Netting/Cashflow
    Auto Netting- 2024.md
  revision: sha256:34c4b38c172ef7151e4940b986c9ad8bf4acb7844cb35adce1a058043cb3dab7
  sha256: 34c4b38c172ef7151e4940b986c9ad8bf4acb7844cb35adce1a058043cb3dab7
- resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home Page/Functional Requirement/Settlement
    Day2 Requirement/Cashflow Auto Netting/Auto Netting Datetime Calculation.md
  revision: sha256:cc523d1571fd9c92465da0edb1f8bffd6e5854e1ade01eb91823eaaaa8dc06f8
  sha256: cc523d1571fd9c92465da0edb1f8bffd6e5854e1ade01eb91823eaaaa8dc06f8
generated:
  by: agent:codex
  at: '2026-11-12T05:15:00.618215+00:00'
verified: []
classification: settlement
scope: Scheduled Cash Settlement auto-netting from rule evaluation to resultant cashflow handling.
summary: Hold cashflows for the matched live rule. Run the scheduled job and group cashflows by rule identity
  and all configured execution key values.
related:
- KT-portal-purpose
open_questions:
- Which effective policy controls scheduling, calendars, and late arrivals for each scope?
- Which effective policy controls rule precedence, refresh, and re-entry after an un-net?
- Which single cashflow outcomes apply by netting type and rule configuration?
---
# Cash Settlement auto-netting

## Scope

This topic covers the intended scheduled auto-netting workflow.
It records the Day 2 requirements and the September 2026 flow description.
Other Netting workflows remain outside this topic.

## Summary

Evaluate an incoming cashflow against live rules.
Hold a matching cashflow for scheduled execution.
Group it with other cashflows only when the rule identity and each value of the execution key match.

## Documented knowledge

### Rule selection and scheduling

A live rule match sends a cashflow to Pending Auto Netting.
The scheduled job picks up the queued cashflow using the configured netting date and time.
[Function Flow](../../../evidence/knowledge/sources/sha256/639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708.md#L24-L33) [Day 2 queue states](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L67-L69)

The Day 2 requirement ranks netting types by the lowest configured priority number.
If matching rules share the same type, select the rule created later.
The September summary also records that an earlier match in the priority order ends evaluation.
[Day 2 rule selection](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L44) [September priority order](../../../evidence/knowledge/sources/sha256/c98ed22769a19102e766f3dbdff3aa41ee52eef7426bef708f083a166b79d396.md#L59-L61)

### Grouping and outcome

The execution key is the configured set of fields used to group cashflows for a netting type.
Two cashflows can net together only when they have the same rule identity and identical values for all fields of that key.
For Bilateral Netting, the documented key is booking entity, counterparty, payment currency, and payment date.
The netting type supplies the mapping used to create the resultant cashflow.
[Execution key and result mapping](../../../evidence/knowledge/sources/sha256/639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708.md#L32-L44) [Day 2 grouping rule](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L42)

If a cashflow has no matching partner, Day 2 directs the job to release it from the queue after the scheduled time and apply the rule's straight-through processing level.
The requirement leaves the Settle as Gross flag unset.
The September summary describes single cashflows as exception cases.
The applicable exception and downstream action require confirmation for each netting type.
[Day 2 single cashflow rule](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L43) [Resultant and exceptions](../../../evidence/knowledge/sources/sha256/c98ed22769a19102e766f3dbdff3aa41ee52eef7426bef708f083a166b79d396.md#L72-L77)

### Dated rule differences

| Subject | Source positions |
| --- | --- |
| Calendar | Day 1 uses the booking entity's home currency calendar. Day 2 uses the cashflow currency calendar and retains the payment date for a VD rule. A later design discussion proposes skipping weekends only. [Day 1 calendar](../../../evidence/knowledge/sources/sha256/34c4b38c172ef7151e4940b986c9ad8bf4acb7844cb35adce1a058043cb3dab7.md#L18) [Day 2 calendar](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L40) [Calendar discussion](../../../evidence/knowledge/sources/sha256/cc523d1571fd9c92465da0edb1f8bffd6e5854e1ade01eb91823eaaaa8dc06f8.md#L34-L37) |
| Late arrivals | Day 1 sends a late arrival to manual netting. The 16 May 2025 Day 2 decision records queueing eligible cashflows before or after the scheduled time. The later design discussion proposes a configurable action. [Day 1 late arrivals](../../../evidence/knowledge/sources/sha256/34c4b38c172ef7151e4940b986c9ad8bf4acb7844cb35adce1a058043cb3dab7.md#L26) [Day 2 review history](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L22) [Day 2 decision](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L74) [Late handling discussion](../../../evidence/knowledge/sources/sha256/cc523d1571fd9c92465da0edb1f8bffd6e5854e1ade01eb91823eaaaa8dc06f8.md#L38) |
| Competing rules | Day 1 prioritizes the earliest scheduled job. The Day 2 main requirement prioritizes netting type and then creation time. An earlier entry in the Day 2 clarification history gives only creation time. [Day 1 priority](../../../evidence/knowledge/sources/sha256/34c4b38c172ef7151e4940b986c9ad8bf4acb7844cb35adce1a058043cb3dab7.md#L20) [Day 2 priority](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L44) [Day 2 history](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L74) |
| Rule changes and re-entry | Day 2 lists refresh behavior for create, update, and disable. Its clarification history also records a no-refresh alternative. The Day 2 single cashflow rule permits re-entry after an operator reinstates it. The September summary says cashflows produced by an un-net do not re-enter auto-netting evaluation. Confirm which behavior applies to each trigger. [Day 2 refresh](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L41) [Refresh alternative](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L65) [Operator reinstatement](../../../evidence/knowledge/sources/sha256/a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62.md#L43) [September un-net handling](../../../evidence/knowledge/sources/sha256/c98ed22769a19102e766f3dbdff3aa41ee52eef7426bef708f083a166b79d396.md#L76) |

## Connections

The [Portal purpose](../background/KT-portal-purpose.md) describes the shared entry and workspace for post-trade applications.
Cash Settlement rules belong to the application domain.

## Evidence limits

The retained requirements, review notes, and flow descriptions support candidate intent.
Their effective business scope and publication approval need domain-owner evidence.
The November calendar discussion records proposals.
The dated differences remain open.

## Open questions

Owner: unknown.

- Which effective policy controls scheduling, calendars, and late arrivals for each scope?
- Which effective policy controls rule precedence, refresh, and re-entry after an un-net?
- Which single cashflow outcomes apply by netting type and rule configuration?
