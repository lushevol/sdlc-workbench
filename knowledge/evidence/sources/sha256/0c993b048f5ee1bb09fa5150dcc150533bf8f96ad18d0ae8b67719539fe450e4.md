# 1. Background

# 2. Requirement

## 2.1 Existing Requirement and Design

## 2.2 BAU Test Cases

[LMS Integration Test case recording]

# 3. Developer Mind Map:

## 3.1 Class Diagram

![image2023-4-19_15-31-41.png](attachments/image2023-4-19_15-31-41.png)

## 3.2

| SN | Business Event Tracking | Topic Listening | Filter logic |
| --- | --- | --- | --- |
| 1 | Lifecycle service publish cashflow event to query service | Cash_Settlement_Orchestration_Process_In | |
| 2 | Cashflow stamping complete | cash_settlement_cashflow_domain_events | |
| 3 | trade service got leid and trader successfully | Trade_Service__Trade_Events | |