# Controls: Test Strategy

---

## Control Attributes

| **Control Name** | Test Strategy |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Test Strategies are established to define the test scope and approach and to identify all testing that is required to verify that the solution operates correctly in the production environment<br/>- Define the adequacy of the testing covering resources, environments, specifications, data requirements, risk and issues. |
| **Control Requirements** |<br/>- Ensure Test Strategies are in place for any new solution<br/>- Ensure Test Strategies are updated for changes to architecture or when major functional changes drive changes to test scope or approach<br/>- Ensure Test Strategies are signed off by stakeholders ahead of commencement of testing |
| **Control Tasks** | Ensure the below are agreed with all the stakeholders (Business, Technology, Vendors)<br/>- Develop Test Strategy with stakeholders (Business, Technology, Vendors) covering:<br/>1. Test Scope: Define the area of the application/product that will be tested as well as types of testing to be performed (Functional, Non-Functional)<br/>2. Test Approach: Determine types of tests to be conducted beyond the test types, their order of execution, and criteria to determine the application is adequately tested.<br/>3. Test Techniques: Determine all test types and applicable test design techniques to be followed (including how they will be executed (Automated, Manual))<br/>4. Test Environments: Determine all the Software, hardware, network configurations, Access controls, Access to the interfacing systems that are required to perform adequate levels of testing.<br/>5. Test Data: Determine test data required and to be loaded, taking into account the conditions to use Production data for testing purpose. |
| **Evidence** | The controls expectations must be met using the Banks standard process & tools. Evidences are accumulated automatically if using the bank's engineering pipeline, any other approach requires manual evidencing and would be treated as Risk sensitive. |

| **#** | **Evidence** | **When** | **Scope** | **Performer** | **Approver** | **Document Update/Review Frequency** | **Evidence - ADO** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Test Strategy | Inception | To define the Testing Scope, Test Approach, Test Techniques, Test Environments and Test Ownership for the solution. For APIs in scope of the solution:<br/>- All **Test Types** are applicable: Unit Test, Functional Test, Integration Test, Performance Test, Acceptance Test and OAT.<br/>- A list of in-scope API endpoints must be explicitly identified in the **API Test Scope** section.<br/>- **API Test Approach section** must capture testing approach that is being applied to the APIs | Test Manager |<br/>1.Product Owner<br/>2.Technology Service Owner |<br/>- Test Strategy once attested is valid only for 12 months.<br/>- Test strategy must exist for each Application services.<br/>- For New applications, Test strategy to be aligned and signed off along with the Application Architecture and Solution Intent. | Signed off test strategy Uploaded as part of Application Work Item |

## Relationships

### Qualified References

- **Disciplines**
  - [Testing](../disciplines/testing.md)

- **Tasks**
  - [Define Test Strategy](../disciplines/testing/define-test-strategy.md)
  - [Review and Sign off Test Strategy](../disciplines/testing/review-and-sign-off-test-strategy.md)

- **Artifacts**
  - [Test Strategy](../work-products/testing/test-strategy.md)

- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Understanding Application Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-application-work-item-in-ado.md)
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [How to do application control evidencing in ADO](../appendix/guidance/how-to-do-application-control-evidencing-in-ado.md)

- **Templates**
  - [Test Strategy](../templates/test-strategy.md)

- **Guidelines**
  - [API Guidelines](../guidance/guidelines-by-discipline/testing/api-guidelines.md)
  - [API Classifications](../guidance/guidelines-by-discipline/testing/api-classifications.md)
  - [API Testing Guidelines](../guidance/guidelines-by-discipline/testing/api-testing-guidelines.md)

- **Checklists**
  - [Release Compliance Controls â€” Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)