---
type: "Concept"
sources: ["summaries/KT-settlement-auto-netting.md"]
description: "Auto-netting groups cashflows by rule identity and execution-key values, then handles the resulting cashflow or unmatched items."
---

# Cashflow Netting Grouping and Outcomes

## Definition

Scheduled auto-netting requires the same matched rule and identical values for every field of the netting type’s configured execution key.

## Grouping rules

A cashflow can net with another only if both conditions hold:

1. They were matched to the same rule identity.
2. Their values match for every field in the execution key configured for that netting type.

For Bilateral Netting, the documented execution key consists of booking entity, counterparty, payment currency, and payment date. The execution key is therefore configuration-dependent; the documented Bilateral fields should not be assumed to apply to every netting type.

## Outcomes

The netting type supplies the mapping used to create the resultant cashflow. If a cashflow has no matching partner, the Day 2 requirement says the scheduled job releases it from the queue after the scheduled time and applies the rule’s straight-through processing level, leaving the Settle as Gross flag unset.

The September flow description characterizes single cashflows as exception cases. The sources do not settle which single-cashflow outcome applies across netting types and rule configurations, so that behavior requires confirmation for the relevant scope.

## Source limits

This concept is based on one source document, [[summaries/KT-settlement-auto-netting]]. The document consolidates candidate requirements and flow descriptions; it does not establish an approved, universally effective policy. In particular, confirm the single-cashflow outcome for each applicable netting type and configuration.
