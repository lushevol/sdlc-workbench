# 1. Background

One of the pain points Ops face is decimal difference on our payments vs Counterparty expectation (due to rounding differences). Generally, Ops team always affirm with clients before value date or on value date. And the modification could be done before cashflow been settled.

Some of the clients are insistent that we need to pay the exact decimal amount as per their books for Audit purpose.

- When our payment amount is higher example: xxxx5.02 on our side vs xxxx5.01 on client side, Setts will split the amount, pay xxxx.01 and suppress the remaining 0.01
- When our payment amount is lower example xxxx7.01 on our side vs xxxx7.02 on client side, Setts team suppress the payment in Ratan and do a manual payment via Oscar.

This has risk of manual error, hence team is requesting a feature to allow increase of payment amount within a threshold (USD 1 equivalent) with maker / checker.

# 2. Requirements

## 2.1 Summary

1. The system shall support a Maker/Checker-based payment amount adjustment before cashflow release.
2. The adjustment is limited to a small difference below the configured USD 1 equivalent threshold and applies only to eligible cashflows and currencies.
3. The adjusted amount shall be used for Swift and LMS downstream messages, while the original amount shall be retained for Accounting.
4. An adjusted cashflow shall not be eligible for further Netting or Splitting until the adjustment is removed and approved.
5. The existing Orchestration/Camunda Maker/Checker flow and APIs should be reused as much as possible.

[See details ： Increase Payment Amount within USD 1 Threshold - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Increase+Payment+Amount+within+USD+1+Threshold#IncreasePaymentAmountwithinUSD1Threshold-Background)

# 3. Technical [Solution Design](https://confluence.global.standardchartered.com/display/DSP/SUSPENDED+RULE+FILTER+in+Ratan+Tech+Design#SUSPENDEDRULEFILTERinRatanTechDesign-SolutionDesign)

The existing Orchestration/Camunda Maker/Checker flow and APIs will be reused. No separate User Task creation flow will be introduced.

4.