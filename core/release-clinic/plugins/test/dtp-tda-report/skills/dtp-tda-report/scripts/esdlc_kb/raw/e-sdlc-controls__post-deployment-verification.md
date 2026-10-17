# Controls: Post Deployment Verification

---

## Control Attributes

| **Control Name** | Post Deployment Verification |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** | Verify that the production deployment is successful and the release is operational from a technical and business perspective. |
| **Control Requirements** |<br/>- Plan and develop test cases for post verification testing to include business processes and operational stability. eg: service health checks, production monitoring in place. Countries Impacted by the Change and Countries Involved in PIT must be the same. If there is discrepancy, justification must be provided.<br/>- Perform post verification testing in the production environment to determine if the release deployed is working as expected and meets all the stakeholder expectations. Evidences provided cover all impacted countries/applications in the Change Record.<br/>- Report verification results and/or any issues found on production.<br/>- Execute roll back if required.<br/>- Agree on Post release monitoring (if applicable) and early life support (if applicable) |
| **Control Tasks** |<br/>1. Define UVT steps and acceptance criteria<br/>1. Note: This is not a substitute for UAT. UVT is performed to check that the production deployment and configuration has been successful and that the core business processes continue to work as expected.<br/>2. Consider a dress rehearsal if there is complexity or criticality, in particular in multi-system rollouts (e.g. core banking conversion etc)<br/>3.<br/>- Perform Technical Verification<br/>- Evaluate deployed release for unintended behaviours against pre-defined control criteria eg: application health checks, verify connectivity to interfacing systems and production monitoring<br/>- Perform User Verification<br/>- Evaluate changed system for business operability and production data integrity.<br/>- If Technical Verification and UVT successful<br/>- Perform required housekeeping such as data clean up to ensure no test transactions/data are in production.<br/>- Ensure CMDB is up-to-date with latest configuration information<br/>- If Technical Verification or UVT fail<br/>- Determine whether rollback is required, and if so bring system back into pre-deployment state<br/>- Provide feedback to - change management in support of change ticket closure - to (Tech) Product Owners based on deployment results (for possible improvements...) of their releases<br/>- Conduct a post-implementation review to confirm outcome and results, identify lessons learned, and develop an action plan where required<br/>- Commence post go-live monitoring and support as per agreement with stakeholder |
| **Evidences** |  |

| **Sl.No** | **Evidences** | **When** | **Scope** | **Performer** | **Approver** | **Document Update/Review Frequency** | **Evidence** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TVT (technical verification test) | Transition | To ensure deployment completed successfully in the target environment | Delivery Team | Technology Support Manager | All technology changes |<br/>- Confirmation on performing TVT by PSS / Delivery Team<br/>- PIT Results in PIT Change Task<br/>- TVT<br/>- Test Results and Evidences |
| 2 | User verification testing (UVT) summary | Transition | To ensure deployment completed successfully in the target environment. | Business Owner | Product Owner | Changes involving end user functionality change |<br/>- Confirmation on performing UVT by Business User<br/>- Countries Involved in UVT<br/>- Rationale if Countries Involved not same as Impacted Countries PIT Results in PIT Change Task. UVT<br/>- Test Results and Evidences. |

## Relationships

### Qualified References

- **Disciplines**
  - [Deployment](../disciplines/deployment.md)

- **Tasks**
  - [CMDB Update (verify)](../disciplines/deployment/cmdb-update-verify.md)
  - [Communicate Deployment Status](../disciplines/deployment/communicate-deployment-status.md)
  - [Monitor and Report Deployment](../disciplines/deployment/monitor-and-report-deployment.md)
  - [Perform ELS](../disciplines/deployment/perform-els.md)
  - [Perform Technical Verification](../disciplines/deployment/perform-technical-verification.md)
  - [Perform Post Implementation Test (PIT)](../disciplines/deployment/perform-post-implementation-test-pit.md)
  - [Review Deployment Completeness](../disciplines/all-tasks/review-deployment-completeness.md)

- **Artifacts**
  - [[Installation Artifacts]](../work-products/operations-amp-support/installation-artifacts.md)
  - [[Operations Artifacts]](../work-products/operations-amp-support/operations-artifacts.md)
  - [Approved Change Request](../work-products/deployment/approved-change-request.md)
  - [Deployment Management Report](../work-products/deployment/deployment-management-report.md)
  - [Deployment Plan](../work-products/deployment/deployment-plan.md)
  - [UVT Scenarios](../work-products/deployment/uvt-scenarios.md)

- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Next Gen Pipeline- ADO - General FAQ](../tools/next-gen-pipeline-ado/next-gen-pipeline-ado-general-faq.md)
  - [Understanding Application Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-application-work-item-in-ado.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [Managing a Release Work Item with multiple Change Requests](../tools/Managing-a-release-work-item-with-multiple-Change-Requests.md)

- **Checklists**
  - [Release Compliance Controls â€” Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)