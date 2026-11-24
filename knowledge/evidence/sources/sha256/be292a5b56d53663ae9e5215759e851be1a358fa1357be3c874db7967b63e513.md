# Business Background

[[Draft]Product Agnostic Aggregation based on Normalized Payment Schedule - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/%5BDraft%5DProduct+Agnostic+Aggregation+based+on+Normalized+Payment+Schedule)

# Workflow

# Group Service

## Keep NormalizedPaymentSchedule jsonNode

Group service will split Uber JSON into multiple JSON messages by Cashflow and send them to workflow. It will keep and send  NormalizedPaymentSchedule elements also if Uber messages contains NormalizedPaymentSchedule element.

## UBER Message sample

![image-2026-8-12_9-48-10.png](attachments/image-2026-8-12_9-48-10.png)

# Rule Engine Service

## Create new rule to block auto aggregation

- new rule_type = "AUTO_AGGREGATION" && business_flow = "STRATEGIC_SETTLEMENT"

1. Entity__Booking_Entity_SCI_FMID in ("300011345", "10038345") && Entity__Counterparty_SCI_FMID in ("10055390", "10037780", "10023033", "205001936")

# Orchestration Service

## Workflow Change

### Flow 1

### Flow 2 Happy flow

# Netting Service

## Process Auto Aggregation

1. count payment schedule elements in NormalizedPaymentSchedule. And filter by cashflow currency and paymentDate. Exclude any Fee elements. Take this as expected_num.
2. Fetch cashflows by tradeId and filter currency and payment date and not "AsGross", get valid cashflow number of this trade as cf_count.
3. Compare expected_num with cf_count, if expected_num > cf_count then cashflow will update to pending another leg. otherwise, will do auto aggregation with these cashflows.

- config in Netting-service

1. Payment Type: *Fee (Cashflow.payment_type will bypass Aggregation process; normalizedPaymentSchedule.payment_type will decrease expected_num)

### Process 1 Happy case

### Process 2

# Foundation Upgrade

## UBER Client libs upgrade

We need upgrade UBER relate packages as normalizedPaymentSchedule is new element.