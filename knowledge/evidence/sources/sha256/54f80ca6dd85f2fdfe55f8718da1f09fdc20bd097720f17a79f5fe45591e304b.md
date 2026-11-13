# Current System Architecture

![image2023-1-6_15-49-11.png](attachments/image2023-1-6_15-49-11.png)

Disadvantage ：

1. Based on DDD, domain should be clear, but currently there are too much service integration and domain service is handling something not belong to it. (for example: maker & checker belong to process domain)
2. Maker & checker hard coded in business services, without chance to adjust flexibly.
3. Services is too heavy and too complex

# Proposal

NSTP Maker-Checker Workflow

![image2023-1-10_22-8-14.png](attachments/image2023-1-10_22-8-14.png)

Adhoc Suppression Maker-Checker workflow

![image2023-1-11_10-43-55.png](attachments/image2023-1-11_10-43-55.png)

# Comparison

| | Current Workflow | Proposed Workflow |
| --- | --- | --- |
| Workflow Visualization | Lowly streamlined. Only main workflow can be seen, most of the Maker-Checker details are implement in code | Highly streamlined, all user operations logic can be seen in workflow |
| Code Intrusive | Intrusive. Maker-checker logic is coupling with the business code in micro-service | Non-Intrusive. Maker-Checker logic is implemented by native Camunda workflow |
| Maintainability | Hard to maintain. If Maker-Checker logic change, code should be changed accordingly and the impacts have been estimated for other logic. For Maker-Checker new requirement, it have been implement in code | Maintainable. If Maker-Checker logic change, only change the Camunda workflow, new Maker-Checker requirement can be implemented in Camunda |
| Complexity | High code complexity. | High Camunda workflow complexity. |
| Independency | Micro-service include workflow logic and business logic as well | Micro-service keeping basic business logic, workflow logic implemented by Camunda |

# Implement Plan

**Target:  2023 Sprint 1 **

| Module | Changes | Estimation |
| --- | --- | --- |
| ratanone-camunda-flow-starter | adding trigger workflow with API request | 2 |
| create a maker API, this API will start a Camunda process by ratanone-camunda-flow-starter | 2 |
| create a checker API, this API will complete a checker user task | 2 |
| provide a API to save cashflow_user_operation_record | 1 |
| add table cashflow_user_operation_record, and provide CRUD functions | 2 |
| ratan-cash-settlement-orchestration | modify 1_5_Nstp_Check.bpmn, If it's a NSTP cashflow, add a sub-workflow in this diagram | 2 |
| ratan-cashflow-lifecycle-service | provide a API to update the scbml history table as Pending_Operator / NSTP_Release for Camunda calling | 1 |
| statusmachine provide a API for camunda calling | 1 |

# User Operation Table

![image2023-1-3_19-3-1.png](attachments/image2023-1-3_19-3-1.png)