# Controls: Non Functional Testing

---

## Control Attributes

| **Control Name** | Non-Functional Testing |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Solutions and or changes have passed acceptance testing for agreed non-functional requirements (Performance, Stability, OAT, Data) ahead of release and subsequent deployment to production environments.<br/>- Existing solutions continue to operate to agreed service level (including stability and performance) criteria |
| **Control Requirements** |<br/>- Non-Functional capabilities must be traceable and tested against agreed non-functional requirements ahead of release.<br/>- Ensure Test Impact Assessments are performed.<br/>- Ensure applicable (non-functional) Test Types, Testing techniques and Test approaches are identified as per Testing Guidelines.<br/>- Ensure evidence for conducted testing is captured and tallies with results signed-off during acceptance testing, this must include some of the following:<br/>&emsp;- Log files<br/>&emsp;- Transaction reports<br/>&emsp;- Screenshots<br/>&emsp;- Automated Test Run Reports<br/>- Verify that the application works as designed and handles errors and unexpected scenarios gracefully.<br/>- Optimize/Improve testing process without compromising the accuracy of the outcome.<br/>- Non-Functional Testing is applicable under the following circumstances.<br/>&emsp;- Significant change in Architecture<br/>&emsp;- Significant Change on Non-Functional Requirements.<br/>- Scope of Non-Functional testing includes<br/>&emsp;- Performance Testing (E2E/Interface, Peak (AKA Regression Performance test) , Stress and Soak)<br/>&emsp;- OAT (Pre-prod acceptance testing)<br/>&emsp;- Data Migration Testing |
| **Control Tasks** |<br/>- Every Change (Code, Architecture, Configuration and interface) needs to be assessed for impact on the system stability and performance outcomes are as follows:<br/>&emsp;- No Testing Needed<br/>&emsp;- Rationale Given<br/>&emsp;- Profile testing<br/>&emsp;- Rationale Given<br/>&emsp;- Peak Test (Performance regression test)<br/>&emsp;- Full Performance Testing<br/>&emsp;- Significant NFR or Architecture Changes<br/>- Undertake tests of system and application performance in accordance with the NFT plan. Consider a range of performance metrics (e.g., end-user response times, Batch window & volume, database and management system)<br/>- Ensure all new applications must undergo non-functional testing prior to being deployed into the production environment (Including Technical Releases)<br/>- Ensure that relevant non-functional testing is conducted periodically at the Application level including all the interfacing applications/services to determine if the required capabilities are working as expected.<br/>- Ensure all Result Analysis is documented appropriately within NFT test reports.<br/>- Including identifying, log and classify (e.g., minor, significant, mission-critical) errors during testing. Ensure that an audit trail of test results is available. In accordance with the test plan, communicate results of testing to stakeholders to facilitate bug fixing and further quality enhancement<br/>- Control Tasks must be carried out using the Banks standard processes and tools.<br/>- Control tasks apply to both internally developed solutions as well as vendor provided solutions.<br/>- All new / existing application releases must undergo non-functional testing prior to being deployed into the production environment (Including Technical Releases)<br/>- Relevant non-functional testing must be conducted periodically at the Application level (including all the interfacing applications / services) to determine if the required capabilities continue working as expected. |
| **Evidence** | The controls expectations must be met using the Banks standard process & tools. Evidence are accumulated automatically if using the bank's engineering pipeline, any other approach requires manual evidencing and would be treated as Risk sensitive. |

| **Sl.No** | **Evidence** | **Scope** | **Performer** | **Approver** | **Document Update/Review Frequency** | **Evidence - ADO** |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Test Plan | NFT Scope-<br/>- Significant change in Architecture<br/>- Significant Change on NFR<br/>- Penetration test<br/>- First Time and Annually<br/>- Data Migration testing when there is a data migration as per the release scope.<br/>- Ensure OAT is conducted before the Production deployment | Delivery team | Technology Service Owner | Performance Testing is required under these conditions:<br/>- Performance Testing is applicable when you onboard the application for the first time.<br/>- When changes occur, conduct Performance Test Impact Assessment as referenced under Testing Guidelines (Performance Testing) to determine whether performance testing is required. |<br/>- Approved PT Plan and Report to be enclosed in the **Application Workitem**. Test Summary Report will be auto generated. |
| 2 | NFT report | Generate Report whenever Partial or full Non functional testing are conducted. | Delivery Team | Technology Service Owner | For each release where performance Testing Takes place or For every Non functional test execution | Test Summary Report will be auto generated. |
| 3 | Test Summary report |  |  |  |  | Test Summary Report will be auto generated. |
| 4 | Rationale | Rationale for not performing the minimum required NFT<br/>- Peak | Delivery Team | Test Manager | For every release where minimum of a peak performance test does not take place. | Release Work item |

## Relationships

### Content References

- [How To - Update a link in Azure Boards?](../tools/next-gen-pipeline-ado/how-to-update-a-link-in-azure-boards.md)


### Qualified References
- **Disciplines**
  - [Testing](../disciplines/testing.md)
- **Tasks**
  - [Complete Performance Test Impact Assessment](../disciplines/testing/complete-performance-test-impact-assessment.md)
  - [Define Performance Test Plan](../disciplines/testing/define-performance-test-plan.md)
  - [Define Test Summary Report](../disciplines/testing/define-test-summary-report.md)
  - [Design Acceptance Tests](../disciplines/testing/design-acceptance-tests.md)
  - [Design and Build Performance Test Scripts](../disciplines/testing/design-and-build-performance-test-scripts.md)
  - [Design Resilience Tests](../disciplines/testing/design-resilience-tests.md)
  - [Design Operational Acceptance Tests](../disciplines/testing/design-operational-acceptance-tests.md)
  - [Design Performance Test](../disciplines/testing/design-performance-test.md)
  - [Design Security Tests](../disciplines/testing/design-security-tests.md)
  - [Execute Acceptance tests and Produce Final report with Sign off](../disciplines/testing/execute-acceptance-tests-and-produce-final-report.md)
  - [Execute Resilience Tests and produce final report with sign off ](../disciplines/testing/execute-resilience-tests-and-produce-final-report.md)
  - [Execute Operational Acceptance Test and Produce Final report with Sign off](../disciplines/testing/execute-operational-acceptance-test-and-produce.md)
  - [Execute Performance Tests and Prepare Performance Test Summary Report](../disciplines/testing/execute-performance-tests-and-prepare-performance.md)
  - [Execute Regression Tests](../disciplines/testing/execute-regression-tests.md)
  - [Execute Security Tests and Produce final report with Sign Off](../disciplines/testing/execute-security-tests-and-produce-final-report.md)
  - [Produce Traceability Report](../disciplines/testing/produce-traceability-report.md)
  - [Review and obtain sign off for performance test plan](../disciplines/testing/review-and-obtain-sign-off-for-performance-test.md)
  - [Review and Obtain Signoff on Test Cases](../disciplines/testing/review-and-obtain-signoff-on-test-cases.md)
  - [Review and sign off Performance Test Impact Assessment](../disciplines/testing/review-and-sign-off-performance-test-impact.md)
  - [Sign-off Test Summary Report](../disciplines/testing/sign-off-test-summary-report.md)
- **Artifacts**
  - [Test Summary Report](../practices/end-to-end-impact-assessment/work-products/test-summary-report.md)
  - [Automated Test Scripts](../work-products/testing/automated-test-scripts.md)
  - [Defects/Open Issues](../work-products/testing/defectsopen-issues.md)
  - [OAT Report](../work-products/testing/oat-report.md)
  - [Performance Test Impact Assessment](../practices/end-to-end-impact-assessment/work-products/performance-test-impact-assessment.md)
  - [Performance Test Scripts](../work-products/testing/performance-test-scripts.md)
  - [Security Tests](../work-products/testing/security-tests.md)
  - [Test Evidence and Results (Security Tests)](../practices/security-in-delivery/work-products/test-evidence-and-results-security-tests.md)
  - [Test Evidences and Results (Acceptance Tests)](../work-products/testing/test-evidences-and-results-acceptance-tests.md)
  - [Test Evidences and Results (Resilience Tests) ](../work-products/testing/test-evidences-and-results-resilience-tests.md)
  - [Test Evidences and Results (Performance Tests)](../work-products/testing/test-evidences-and-results-performance-tests.md)
  - [Test Evidences and Results (Regression Tests)](../work-products/testing/test-evidences-and-results-regression-tests.md)
  - [Test Final Report (Performance Test)](../work-products/testing/test-final-report-performance-test.md)
  - [Test Plan (Performance Test)](../work-products/testing/test-plan-performance-test.md)
  - [Test Report (SAT)](../practices/security-in-delivery/work-products/test-report-sat.md)
  - [Test Scenarios & Cases (Acceptance Tests)](../work-products/testing/test-scenarios-amp-cases-acceptance-tests.md)
  - [Test Scenarios & Cases (Availability and Recovery Test)](../work-products/testing/test-scenarios-amp-cases-availability-and.md)
  - [Test Scenarios & Cases (Performance Tests)](../work-products/testing/test-scenarios-amp-cases-performance-tests.md)
  - [Test Scenarios & Cases (Regression Tests)](../work-products/testing/test-scenarios-amp-cases-regression-tests.md)
  - [Traceability Report](../work-products/testing/traceability-report.md)
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
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [Understanding Test Case Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-case-work-item-in-ado.md)
  - [Understanding Test Plan Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-plan-work-item-in-ado.md)
  - [Understanding Test Suite Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-test-suite-work-item-in-ado.md)
  - [What is Azure Test Plans?](../tools/next-gen-pipeline-ado/what-is-azure-test-plans.md)
  - [VX ESDLC Control - Test Closure Report](../appendix/guidance/vx-esdlc-control-test-closure-report.md)
  - [VX ESDLC Control - Test Evidence](../appendix/guidance/vx-esdlc-control-test-evidence.md)
  - [VX ESDLC Control - Traceability Report Maintained](../appendix/guidance/vx-esdlc-control-traceability-report-maintained.md)
  - [How to run manual test cases in ADO](../appendix/guidance/how-to-run-manual-test-cases-in-ado.md)
- **Templates**
  - [Performance Test Impact Assessment](../templates/performance-test-impact-assessment.md)
- **Guidelines**
  - [Bug Management Pipeline Controls User Guide](../guidance/guidelines-by-discipline/testing/Bug-Management-Pipeline-Controls-User-Guide.md)
  - [Test Conditions & Cases](../templates/test-conditions-amp-cases.md)
  - [Test Summary Report](../templates/test-summary-report.md)
  - [Traceability Report](../templates/traceability-report.md)
  - [Performance Test Final Report](../templates/performance-test-final-report.md)
  - [Performance Test Plan](../templates/performance-test-plan.md)
- **Checklists**
  - [Test Case Review Checkist](../checklist/test-case-review-checkist.md)
  - [Release Compliance Controls — Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)
- **Guidelines**
  - [Test Case Design Techniques](../disciplines/testing/test-case-design-techniques.md)
  - [Detailed Testing Guidelines](../disciplines/testing/detailed-testing-guidelines.md)
  - [Testing type Guidelines](../disciplines/testing/testing-type-guidelines.md)
  - [Test Environment Management – Vendor Managed Applications](../disciplines/test-environment-management/test-environment-management-vendor-managed.md)
  - [Vendor Products Testing Guidelines](../guidance/guidelines-by-discipline/testing/vendor-products-testing-guidelines.md)
  - [API Classifications](../guidance/guidelines-by-discipline/testing/api-classifications.md)
  - [API Guidelines](../guidance/guidelines-by-discipline/testing/api-guidelines.md)
  - [API Testing Guidelines](../guidance/guidelines-by-discipline/testing/api-testing-guidelines.md)