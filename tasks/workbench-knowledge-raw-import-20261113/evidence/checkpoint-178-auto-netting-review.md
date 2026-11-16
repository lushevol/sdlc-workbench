# Auto-netting candidate review

Status: SUPPORTED_WITH_LIMITS.
Actor: agent:sol-auto-netting-review.
Semantic review time: 2026-11-16T08:38:52.022397+08:00.
Candidate SHA-256: `ca7ff52d0e4303639a9a429584112eae3bdfc9a26f35abb45c4d0456e1f6cfe4`.

The eight source declarations are supported. The candidate body is unchanged.
All thirteen declarations match unique manifest tuples. All five retained snapshot hashes match.
The review supports dated candidate intent. It does not establish effective policy or publication approval.

Native worker selection uses the requested GPT-6.1 Sol and medium reasoning.
Independent runtime attestation is unavailable and is not claimed.

| Claim | Evidence and rationale |
| --- | --- |
| C1: A live-rule match queues the cashflow; the scheduled job uses configured netting date and time. | 639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708: L24–L33; a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L67–L69. Flow rows explicitly record LIVE eligibility, waiting, and scheduled pickup. Day 2 names Pending Auto Netting. |
| C2: Day 2 prioritizes the lowest netting-type priority number, then the later-created rule within one type. | a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L44–L44; c98ed22769a19102e766f3dbdff3aa41ee52eef7426bef708f083a166b79d396: L59–L61. Day 2 states both ordered predicates. September supports short-circuit evaluation but does not independently establish the within-type tiebreaker. |
| C3: Grouping requires the same rule identity and equal values for all configured execution-key fields. | 639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708: L32–L44; a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L42–L42. Flow requires execution-key equality. Day 2 expressly prohibits cross-rule netting and adds the unique rule identifier. |
| C4: Bilateral execution key contains booking entity, counterparty, currency, and payment date; the type supplies resultant mapping. | 639c9cb073bbf7501c7b6a8dc4e0be3c34683ab4cbc4357c2d798ef579b46708: L33–L55; a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L34–L34. Flow text and bilateral matrix row identify these fields. The resultant mapping is configured by type. |
| C5: Day 2 releases a single cashflow after scheduled time with configured STP, without settleAsGross; September records exception handling. | a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L43–L43; c98ed22769a19102e766f3dbdff3aa41ee52eef7426bef708f083a166b79d396: L72–L77. Day 2 states all three conditions and permits reinstatement. September separately labels single-cashflow exceptions. Candidate does not select a universal outcome. |
| C6: Sources retain competing calendar rules. | 34c4b38c172ef7151e4940b986c9ad8bf4acb7844cb35adce1a058043cb3dab7: L18–L18; a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L40–L40; cc523d1571fd9c92465da0edb1f8bffd6e5854e1ade01eb91823eaaaa8dc06f8: L34–L38. Day 1 uses booking-entity home-currency calendar. Day 2 uses cashflow currency and preserves VD. Solution Discussion proposes skipping weekends, with holiday and release-date tradeoffs. |
| C7: Sources retain competing late-arrival handling. | 34c4b38c172ef7151e4940b986c9ad8bf4acb7844cb35adce1a058043cb3dab7: L26–L26; a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L22–L22, L74–L74; cc523d1571fd9c92465da0edb1f8bffd6e5854e1ade01eb91823eaaaa8dc06f8: L34–L38. Day 1 routes late flows manually. Dated 16 May 2025 text records holding before or after cutoff. Discussion proposes configurable manual versus auto handling. |
| C8: Sources retain competing precedence rules. | 34c4b38c172ef7151e4940b986c9ad8bf4acb7844cb35adce1a058043cb3dab7: L20–L20; a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L44–L44, L74–L74. Day 1 selects earliest scheduled job. Day 2 main text adds type priority; earlier clarification history selects latest-created rule only. |
| C9: Sources retain competing refresh and re-entry rules. | a877fc303ccf2ad4a8a209d7a40faaa2dfa5f522eaba917726aa79b0e1433b62: L41–L43, L65–L65, L74–L76; c98ed22769a19102e766f3dbdff3aa41ee52eef7426bef708f083a166b79d396: L29–L31, L76–L76. Main Day 2 refresh details differ from no-refresh history. Reinstated singleton re-entry and historical un-net eligibility differ from September no-re-entry. Candidate asks for trigger-specific applicability. |

Effective calendars, cutoff handling, precedence, refresh, re-entry, and singleton outcomes remain unresolved.
Owner: unknown. Obtain domain-owner scope and effective-date evidence before selecting a governing policy.

The newer flow selection omits some cited ranges. The retained earlier selection includes them.
Added declarations do not broaden selection authority. Retain both contexts for later reconciliation.
Manifest classifications remain unknown. Ingest timestamps do not establish policy dates or approval.

No material unsupported current assertion requires correction within this candidate scope.
The candidate explicitly preserves dated differences and requires domain-owner confirmation.

Automated checks verified candidate hashes, snapshot hashes, tuple uniqueness, proposal additions, and unchanged body.
No business execution, deployment, or unrelated record review occurred.
No canonical, audit, receipt, or wiki files changed.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
