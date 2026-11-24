# 1. background

A new requirement asks to map currency SGD to SGO before downstream processing and delivery, so all consumers use a consistent currency code.

# 2. Solution 1 (Implement in Group Management)

## 2.1 Scope

## Implement the currency conversion rule inside Group Management only.

Do not implement this rule in Netting Service for this option.

2.2 Flow Diagram

## 2.2 Implementation Approach

1. **Add a new command** in the Standardization Module to handle currency alias conversion (SGD -> SGO).
2. Register this command in the existing standardization command pipeline (configured in UberHandlerBeanConfig).
3. Make sure it runs before currency-dependent commands (e.g., rounding/cutoff), by assigning an earlier order.
4. From StandardizationCommand, default getOrder() is 1, so the new currency command should use an earlier order (commonly 0).

## 2.3 Main Change Points

1. Add one new command class under domain/standardize.
2. Register the command in standardizationCommands(...) in UberHandlerBeanConfig.
3. No external API contract changes.
## 2.4 Key Risks

1. Downstream cannot feel the change in currency

2. manual netting cannot see the difference in currency

## 2.5 Estimated Effort

Development: Medium
Testing/validation: High

# 3. Solution 2 (Implement in Netting Service)

## 3.1 Scope

Implement the currency alias conversion rule inside Netting Service only.
## 3.2 change logic

| cover logic | change point |
| --- | --- |
| **Manual Netting + Validators + grouping** | CashFlowRepository.getCashFlowQueryResults() |
| **IRS** | NettingService.getWaitingAnotherLegCashflowByTrade() |
| **Auto-netting** | ruleCheck() |

1.Add a currency normalization utility in Netting Service (e.g., alias map SGD -> SGO).
2**.Invoke normalization immediately after cashFlowApiClient.getCashFlowsV2**(...) returns in CashFlowRepository.
3.Normalize CashFlowQueryResult.settlementCurrency before downstream grouping/validation logic.
4**.Extend normalization to IRS flow and Auto-netting rule-check flow**

## 3.3 Main Change Points

1. Add one utility/component for currency alias mapping (e.g., domain/standardize or infra/util in Netting Service).
2. Update CashFlowRepository.getCashFlowQueryResults(...) to apply normalization right after cashFlowApiClient.getCashFlowsV2(...).
3. Update IRS logic in NettingService.

- processIRSNetting(...)
- getWaitingAnotherLegCashflowByTrade(...)

4. Update Auto-netting rule logic

- AutoNettingRuleCheckService.generateAutoNettingCashflow(...)
- AutoNettingRuleCheckService.caculateNettingTriggerTime(...)
- AutoNettingCashflow.generateGroupKey(...)

## 3.4 Key Risks

1. There are many changes, High development cost.
2. Need to verification netting Validator logic for different currencies
3. High testing costs.

## 3.5 Estimated Effort

Development: Low
Testing/validation: Medium