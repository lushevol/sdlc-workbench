# Controls: Functional Testing

---

## Control Attributes

| **Control Name** | Functional Testing |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Solutions and or changes have passed acceptance testing for agreed functional requirements ahead of release and subsequent deployment to production environments. |
| **Control Requirements** |<br/>- Test Impact Assessments are conducted, Test types and [Testing techniques](../guidance/all-guidelines/test-case-design-techniques.md) approaches are identified and planned as per the [Testing Guidelines](../guidance/all-guidelines/testing-type-guidelines.md)<br/>- Functional capabilities must be traceable and tested against agreed functional requirements ahead of release<br/>- Ensure applicable (functional) Test Types, [Testing techniques](../guidance/all-guidelines/test-case-design-techniques.md) and Test approaches are identified as per [Testing Guidelines](../guidance/all-guidelines/testing-type-guidelines.md).<br/>- Ensure evidence for conducted testing is captured<br/>- Ensure defects are identified and tracked for each release. |
| **Control Tasks** |<br/>- Conduct functional testing based on agreed scope and functional acceptance criteria.<br/>- Ensure testing is conducted in an appropriate Test Environment conducive of the intended production environment.<br/>- Capture corresponding test evidence which shows PASS/FAILED status<br/>- Capture corresponding test evidence which must include some of the following:<br/>&emsp;- Log files<br/>&emsp;- Transaction reports<br/>&emsp;- Screenshots<br/>&emsp;- Automated Test Run Report<br/>- Ensure that the application works as designed and handles errors and unexpected scenarios gracefully.<br/>- Verify completeness of coverage of agreed functional requirements for building and testing. Resolve any possible gaps with the stakeholders.<br/>- Ensure traceability from business and functional requirements to test scenarios, test cases and test evidence and known defects.<br/>- Provide a Test Summary Report capturing all planned and conducted testing against agreed requirements to stakeholders a<br/>- Include description of configuration of test environment used for achieving the test results.<br/>- Include list of known defects.<br/>- Get formal sign-off from stakeholders against agreed acceptance criteria<br/>- Where defects exist, a risk assessment is to be performed by the stakeholders ahead of acceptance. Notes:<br/>- Control Tasks must be carried out using the Banks standard processes and tools.<br/>- Control tasks apply to both internally developed solutions as well as vendor provided solutions.<br/>- Releases related to APIs must conduct functional testing.<br/>- For details refer to [API Testing Guidelines](../guidance/all-guidelines/api-testing-guidelines.md) |
| **Evidence** | The controls expectations must be met using the Banks standard process & tools. Evidences are accumulated automatically if using the bank's engineering pipeline, any other approach requires manual evidencing and would be treated as Risk sensitive. |

| **Sl.No** | **Evidences** | **When** | **Scope** | **Performer** | **Approver** | **Document Update/Review Frequency** | **Evidence - ADO** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Test Summary Report | Transition |<br/>- Identified Applicable [Testing type Guidelines](../guidance/all-guidelines/testing-type-guidelines.md) for the release.<br/>- Completion of all the test cases and test types.<br/>- Follow prescribed [Test Case Design Techniques](../guidance/all-guidelines/test-case-design-techniques.md)<br/>- Trace of all the requirements and the associated test results are available.<br/>- [Test Environment Management](test-environment-management.md) on which the testing is performed. (Includes [Vendor test environments](../guidance/all-guidelines/test-environment-management-vendor-managed.md))<br/>- Test results and defects are reported and closed | Delivery Team |<br/>- Product Owner<br/>- Technology Service Owner | Every release |<br/>- Test Summary Report automatically generated in ADO<br/>- All in-scope test cases for the release are mapped<br/>- All in-scope test cases for the release are executed and have passed test results.<br/>- ADO Release Work item link referenced in change request ticket. |
| 2 | Traceability | Construction | Maintain traceability from all in-scope requirements / user stories to test cases and test results. | Delivery Team | This will be covered as a part of ADO Test summary report | Every release | This will be covered as a part of ADO Test summary report |
| 3 | Test Evidences | Construction | Actual test evidences is available for all in-scope testing. This consists of evidence that the tests were executed and provides results of the testing. Eg: log files, screenshots, automated test script runs. | Delivery Team | This will be covered as a part of ADO Test summary report | Every release | This will be covered as a part of ADO Test summary report |

## Relationships

### Content References

- [Execute Resilience Tests and produce final report with sign off ](../disciplines/testing/execute-resilience-tests-and-produce-final-report.md)


- [How To - Update a link in Azure Boards?](../tools/next-gen-pipeline-ado/how-to-update-a-link-in-azure-boards.md)


### Qualified References
- **Disciplines**
  - [Testing](../disciplines/testing.md)
- **Tasks**
  - [Define Test Summary Report](../disciplines/testing/define-test-summary-report.md)
  - [Design Acceptance Tests](../disciplines/testing/design-acceptance-tests.md)
  - [Design Functional Tests](../disciplines/testing/design-functional-tests.md)
  - [Execute Acceptance tests and Produce Final report with Sign off](../disciplines/testing/execute-acceptance-tests-and-produce-final-report.md)
  - [Execute Functional Test](../disciplines/testing/execute-functional-test.md)
  - [Execute Regression Tests](../disciplines/testing/execute-regression-tests.md)
  - [Produce Traceability Report](../disciplines/testing/produce-traceability-report.md)
  - [Review and Obtain Signoff on Test Cases](../disciplines/testing/review-and-obtain-signoff-on-test-cases.md)
  - [Sign-off Test Summary Report](../disciplines/testing/sign-off-test-summary-report.md)
- **Artifacts**
  - [Automated Test Scripts](../work-products/testing/automated-test-scripts.md)
  - [Test Summary Report](../practices/end-to-end-impact-assessment/work-products/test-summary-report.md)
  - [Test Evidences and Results (Acceptance Tests)](../work-products/testing/test-evidences-and-results-acceptance-tests.md)
  - [Test Evidences and Results (Functional Tests)](../work-products/testing/test-evidences-and-results-functional-tests.md)
  - [Test Evidences and Results (Regression Tests)](../work-products/testing/test-evidences-and-results-regression-tests.md)
  - [Test Scenarios & Cases (Acceptance Tests)](../work-products/testing/test-scenarios-amp-cases-acceptance-tests.md)
  - [Test Scenarios & Cases (Functional Tests)](../work-products/testing/test-scenarios-amp-cases-functional-tests.md)
  - [Test Scenarios & Cases (Regression Tests)](../work-products/testing/test-scenarios-amp-cases-regression-tests.md)
- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Next Gen Pipeline- ADO - General FAQ](../tools/next-gen-pipeline-ado/next-gen-pipeline-ado-general-faq.md)
  - [How To - Create a query in Azure Boards?](../tools/next-gen-pipeline-ado/how-to-create-a-query-in-azure-boards.md)
  - [How to - Create manual test cases in ADO](../tools/next-gen-pipeline-ado/how-to-create-manual-test-cases-in-ado.md)
  - [How To - Link work items in Azure Boards?](../tools/next-gen-pipeline-ado/how-to-link-work-items-in-azure-boards.md)
  - [How To - Upload an attachments in Azure Boards?](../tools/next-gen-pipeline-ado/how-to-upload-an-attachments-in-azure-boards.md)
  - [Know more about User Access](../tools/next-gen-pipeline-ado/know-more-about-user-access.md)
  - [Understanding Application Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-application-work-item-in-ado.md)
  - [Understanding Bug Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-bug-work-item-in-ado.md)
  - [Understanding of ADO RBAC](../tools/next-gen-pipeline-ado/understanding-of-ado-rbac.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [Understanding Story Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-story-work-item-in-ado.md)
  - [Understanding Test Case Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-case-work-item-in-ado.md)
  - [Understanding Test Plan Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-plan-work-item-in-ado.md)
  - [Understanding Test Suite Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-suite-work-item-in-ado.md)
  - [VX ESDLC Control - Test Closure Report](../appendix/guidance/vx-esdlc-control-test-closure-report.md)
  - [VX ESDLC Control - Test Evidence](../appendix/guidance/vx-esdlc-control-test-evidence.md)
  - [VX ESDLC Control - Traceability Report Maintained](../appendix/guidance/vx-esdlc-control-traceability-report-maintained.md)
  - [What is Azure Test Plans?](../tools/next-gen-pipeline-ado/what-is-azure-test-plans.md)
  - [How to run manual test cases in ADO](../appendix/guidance/how-to-run-manual-test-cases-in-ado.md)
- **Templates**
  - [Test Conditions & Cases](../templates/test-conditions-amp-cases.md)
  - [Test Summary Report](../templates/test-summary-report.md)
  - [Traceability Report](../templates/traceability-report.md)
- **Checklists**
  - [Test Case Review Checkist](../checklist/test-case-review-checkist.md)
  - [Release Compliance Controls — Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)
- **Guidelines**
  - [Bug Management Pipeline Controls User Guide](../guidance/guidelines-by-discipline/testing/Bug-Management-Pipeline-Controls-User-Guide.md)
  - [Detailed Testing Guidelines](../disciplines/testing/detailed-testing-guidelines.md)
  - [Testing type Guidelines](../disciplines/testing/testing-type-guidelines.md)
  - [Test Case Design Techniques](../disciplines/testing/test-case-design-techniques.md)
  - [Test Environment Management – Vendor Managed Applications](../disciplines/test-environment-management/test-environment-management-vendor-managed.md)
  - [Vendor Products Testing Guidelines](../guidance/guidelines-by-discipline/testing/vendor-products-testing-guidelines.md)
  - [API Classifications](../guidance/guidelines-by-discipline/testing/api-classifications.md)
  - [API Guidelines](../guidance/guidelines-by-discipline/testing/api-guidelines.md)
  - [API Testing Guidelines](../guidance/guidelines-by-discipline/testing/api-testing-guidelines.md)