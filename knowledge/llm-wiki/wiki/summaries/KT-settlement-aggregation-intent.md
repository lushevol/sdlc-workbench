---
type: Summary
description: "Summarizes candidate IRS settlement aggregation actions, schedule counting, grouping, and resultant behavior."
doc_type: short
full_text: sources/KT-settlement-aggregation-intent.md
---

# Settlement aggregation intent

> **Source status:** Candidate/draft. The proposal does not establish current aggregation policy or deployed state transitions.

A dedicated IRS aggregation proposal separates `Aggregate`, `AggregateNew`, and `UnAggregate` from user netting. Eligible components move to AGGREGATED; a new resultant is QUEUED; unaggregation returns components to QUEUED and marks listed resultants DEAD. [Dedicated aggregation proposal](../../../records/candidates/settlement/KT-settlement-aggregation-intent.md#dedicated-aggregation-proposal)

A product-agnostic design counts schedule entries only when payment currency and date match. It covers IRS/CCS legs, coupon/principal currency preference, additional payments, and amortization, but leaves amortization currency cells blank. Four expected payments is an example, not a product-wide limit. The proposed grouping key is trade ID, date, currency, entity, and counterparty; the resultant may then enter netting. [Expected schedule count](../../../records/candidates/settlement/KT-settlement-aggregation-intent.md#expected-schedule-count) [Completion and grouping](../../../records/candidates/settlement/KT-settlement-aggregation-intent.md#completion-and-grouping)

Duplicate, cancelled, amended, delayed, fee, and incomplete schedules lack complete treatment. Confirm the action vocabulary, downstream feeds, resultant permissions, and whether manual unaggregation is required. See proposed [[summaries/KT-settlement-interest-and-nds-netting]].
