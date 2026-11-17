# Background

The system currently provides a Net function that allows users to merge different cashflows. For IRS, the two leg cashflows must be combined automatically for settlement. Since the upstream does not send a pre‑merged cashflow, the system leverages the Net function to perform this merge. While it works functionally, it causes business‑meaning confusion because Net implies a user‑initiated merge of unrelated cashflows.

To remove this ambiguity and reflect the IRS use case correctly, we propose introducing a dedicated Aggregation function specifically for combining the two IRS legs for settlement. This keeps the Net feature semantically clear while supporting the required IRS behavior.

# Change Details

1. New Action and new status
2. | Source Cashflow Status | Source Cashflow Sub Status | Source Cashflow Sub Status Type | Action | Target Cashflow Status | Target Cashflow Sub Status | Target Cashflow Sub Status Type | | --- | --- | --- | --- | --- | --- | --- | | WAITING | Pending Operator | Pending Another Leg | Aggregate | AGGREGATED | NA | NA | | QUEUED | NA | NA | Aggregate | AGGREGATED | NA | NA | | NA | NA | NA | AggregateNew | QUEUED | NA | NA | | AGGREGATED | NA | NA | UnAggregate | QUEUED | NA | NA | | QUEUED WAITING HOLD FAILED SWIFT_SUPPRESSED CASHFLOW_SUPPRESSED READY | ALL | ALL | UnAggregate | DEAD | NA | NA |
3. will manual unaggregate required?
4. user filters, downstream impact (TLM TBC, considering the impact to LMS if we send waiting cashflow feed, CIS for PM ccy)