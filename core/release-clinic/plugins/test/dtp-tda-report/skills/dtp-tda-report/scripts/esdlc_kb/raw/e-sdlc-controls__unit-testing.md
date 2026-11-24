# Controls: Unit Testing

---

## Control Attributes

| **Control Name** | Unit Testing |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Code is functioning to agreed requirements.<br/>- Defects are detected early to minimize development cost. |
| **Control Requirements** |<br/>- Identify unit test cases for all the code changes.<br/>- All unit tests have been executed and passed.<br/>- Code Coverage should be within the metric threshold defined in approved E-SDLC quality gate - [Code Quality and Code Coverage Metrics](https://confluence.global.standardchartered.com/display/SDF/Code%20Quality%20and%20Code%20Coverage%20Metrics)<br/>- All the logs and results/evidence are maintained. |
| **Control Tasks** |<br/>- For SCB solutions<br/>1. Perform Unit Testing in the development environment for all incremental code changes/inclusions.<br/>- For Vendor solutions<br/>1. Establish contractual commitments from the Vendors on all the deliverables for meeting the required quality standards.<br/>2. Gather evidence for adherence ahead of integration or acceptance Note:<br/>- For SCB developed code and where source code is provided to the bank for integration: Control Tasks must be carried out using the Banks standard processes and tools.<br/>- Releases related to APIs must conduct unit and pass testing.<br/>- For details refer to [API Testing Guidelines](../guidance/all-guidelines/api-testing-guidelines.md)<br/>- Unit Test control is mandatory where the code resides in a repository containing production code. It is optional if the code is for a POC. |
| **Evidence** | The controls expectations must be met using the Banks standard process & tools. Evidences are accumulated automatically if using the bank's engineering pipeline, any other approach requires manual evidencing and would be treated as Risk sensitive. |

| **Sl.No** | **Evidences** | **When** | **Scope** | **Performer** | **Document Update/Review Frequency** | **Evidence - ADO** |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |<br/>- Unit Test Cases<br/>- Unit Test Execution results<br/>- Unit Test Coverage report **Note**: Unit test coverage refers to code level coverage that measures both line of code coverage and condition/branch coverage. | Construction | To ensure code is unit tested before system testing | Delivery Team | Whenever there is a change in Code |<br/>- UT code-level tests cases must be stored in ADO repo<br/>- UT test results must be executed via ADO pipeline<br/>- UT Test coverage must meet the metrics defined in the approved E-SDLC quality gate and is available via SonarQube. |

## Relationships

### Qualified References

- **Disciplines**
  - [Testing](../disciplines/testing.md)

- **Tasks**
  - [Execute Unit Tests](../disciplines/testing/execute-unit-tests.md)
  - [Produce Traceability Report](../disciplines/testing/produce-traceability-report.md)

- **Artifacts**
  - [API Technical Specification](../work-products/analysis-amp-design/api-technical-specification.md)
  - [Test Evidences and Results (Unit Tests)](../work-products/testing/test-evidences-and-results-unit-tests.md)
  - [Test Scenarios & Cases (Unit Test)](../work-products/implementation/test-scenarios-amp-cases-unit-test.md)
  - [Traceability Report](../work-products/testing/traceability-report.md)
  - [Unit Tested Code](../work-products/implementation/unit-tested-code.md)

- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Understanding of E-SDLC-Unit Testing, Code Quality & SAST](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-unit-testing-code-quality.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [Understanding Test Case Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-case-work-item-in-ado.md)
  - [Understanding Test Plan Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-plan-work-item-in-ado.md)
  - [Understanding Test Suite Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-suite-work-item-in-ado.md)

- **Guidelines**
  - [Code Quality and Code Security Guidelines](../guidance/all-guidelines/code-quality-and-code-security-guidelines.md)
  - [Detailed Testing Guidelines](../disciplines/testing/detailed-testing-guidelines.md)
  - [Test Case Design Techniques](../disciplines/testing/test-case-design-techniques.md)
  - [Test-Driven Development Guidelines](../guidance/guidelines-by-discipline/development/test-driven-development-guidelines.md)
  - [API Classifications](../guidance/guidelines-by-discipline/testing/api-classifications.md)
  - [API Guidelines](../guidance/guidelines-by-discipline/testing/api-guidelines.md)
  - [API Testing Guidelines](../guidance/guidelines-by-discipline/testing/api-testing-guidelines.md)

- **Metrics and Measurements**
  - [Code Quality and Code Coverage Metrics](../guidance/supporting-materials/code-quality-and-code-coverage-metrics.md)
- **Checklists**
  - [Release Compliance Controls â€” Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)