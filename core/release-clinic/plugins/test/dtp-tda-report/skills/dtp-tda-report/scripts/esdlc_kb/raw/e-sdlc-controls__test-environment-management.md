
# Controls: Test Environment Management

---

## Control Attributes

| **Control Name** | Test Environment Management |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Test Environments are established and maintained to ensure that the individual and integrated solution components can be tested for conformance with requirements and standards.<br/>- Test environments are representative of the ‘live’ production situation to enable testing under 'production like' conditions. |
| **Control Requirements** |<br/>- Test environment demands are assessed, specifications are identified and provisioned based on the requirements.<br/>- Ensure Test Environments are representative of intended target production environments for the release<br/>- Test environments are access controlled to prevent unauthorized changes to the test environment.<br/>- Ensure Test Environments are monitored and healthy for the following test cycles:<br/>&emsp;- Integration Testing<br/>&emsp;- Acceptance Testing (OAT, UAT)<br/>&emsp;- Performance Testing<br/>- Ensure Test Environment monitoring is automated (in line with subsequent production expectations)<br/>- Ensure Test Environments are regularly backed up if they are supporting critical (BC4 and BC5) applications or for applications where frequent delivery occurs. |
| **Control Tasks** |<br/>- Prepare Test Environment Specification for configuration required to ensure validity of testing. As input:<br/>&emsp;1. Review new/revised non-functional requirements.<br/>&emsp;2. Review existing and revised Service Level targets.<br/>&emsp;3. Review existing production setup and envisioned target configuration for production.<br/>- Request / Provision Test Environment based on required specifications. |
| **Evidence** | The controls expectations must be met using the Banks standard process & tools. Evidence are accumulated automatically if using the bank's engineering pipeline, any other approach requires manual evidencing and would be treated as Risk sensitive. |

| **SL.No** | **Evidence** | **When** | **Performer** | **Approver** | **Document Update/Review Frequency** | **Evidence - ADO** |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Test Environment Specifications | Design | Test Engineer | Technology Support Manager | Whenever required / 12 months | Test Environment Specification document declare as part of the test environment tab in Application WI. |

Note:Test Environment Specifications evidence is exempted for SaaS applications fully hosted and managed by vendors.

## Relationships

### Qualified References

- **Disciplines**
  - [Test Environment Management](../disciplines/test-environment-management.md)

- **Tasks**
  - [Automated Application Deployment to Test Environment](../disciplines/test-environment-management/automated-application-deployment-to-test.md)
  - [Complete Test Environment Booking](../disciplines/test-environment-management/complete-test-environment-booking.md)
  - [Complete Test Environment Readiness](../disciplines/test-environment-management/complete-test-environment-readiness.md)
  - [Create Initiatives and obtain access to funds](../disciplines/test-environment-management/create-initiatives-and-obtain-access-to-funds.md)
  - [Define Test Environment Automation Strategy and Tool Selection](../disciplines/test-environment-management/define-test-environment-automation-strategy-and.md)
  - [Develop and formally review Test Environment Specifications](../disciplines/test-environment-management/develop-and-formally-review-test-environment.md)
  - [Develop and obtain sign-off on the High level Test Environment Requirements](../disciplines/test-environment-management/develop-and-obtain-sign-off-on-the-high-level.md)
  - [Identify Test Environment issues, risks and plan mitigation](../disciplines/test-environment-management/identify-test-environment-issues-risks-and-plan.md)
  - [Implement Access Control to the Test Environments](../disciplines/test-environment-management/implement-access-control-to-the-test-environments.md)
  - [Obtain sign-off on Test Environment Specifications](../disciplines/test-environment-management/obtain-sign-off-on-test-environment-specifications.md)
  - [Perform Test Environment Monitoring](../disciplines/test-environment-management/perform-test-environment-monitoring.md)
  - [Procure Software & Hardware (Test Environment)](../disciplines/test-environment-management/procure-software-amp-hardware-test-environment.md)
  - [Provide Test Environment Support](../disciplines/test-environment-management/provide-test-environment-support.md)
  - [Setup Acceptance Test Environment and Data](../disciplines/test-environment-management/setup-acceptance-test-environment-and-data.md)
  - [Setup Integration Test Environment and Data](../disciplines/test-environment-management/setup-integration-test-environment-and-data.md)
  - [Setup Performance Test (PT) Environment and Data](../disciplines/test-environment-management/setup-performance-test-pt-environment-and-data.md)
  - [Track Test Environment Configuration](../disciplines/test-environment-management/track-test-environment-configuration.md)
  - [Validate and certify the Test Environment](../disciplines/test-environment-management/validate-and-certify-the-test-environment.md)

- **Artifacts**
  - [High level Test Environment Requirements](../work-products/test-environment-management/high-level-test-environment-requirements.md)
  - [Test Environment Configuration Tracker](../work-products/test-environment-management/test-environment-configuration-tracker.md)
  - [Test Environment Readiness Checklist](../work-products/test-environment-management/test-environment-readiness-checklist.md)
  - [Test Environment Specifications](../work-products/test-environment-management/test-environment-specifications.md)
  - [Test Environment Access Control](../work-products/test-environment-management/test-environment-access-control.md)

- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Understanding Application Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-application-work-item-in-ado.md)
  - [Understanding of ADO RBAC](../tools/next-gen-pipeline-ado/understanding-of-ado-rbac.md)
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [How to do application control evidencing in ADO](../appendix/guidance/how-to-do-application-control-evidencing-in-ado.md)

- **Templates**
  - [Test Environment Specifications Template](../templates/test-environment-specifications-template.md)

- **Guidelines**
  - [API Testing Guidelines](../guidance/guidelines-by-discipline/testing/api-testing-guidelines.md)
  - [Test Environment Definitions](../disciplines/test-environment-management/test-environment-definitions.md)
  - [Test Environment Management – Vendor Managed Applications](../disciplines/test-environment-management/test-environment-management-vendor-managed.md)
  - [Test Environment Management Operating Model](../guidance/guidelines-by-discipline/test-environment-management/test-environment-management-operating-model.md)
  - [Test Environment Management Standards](../disciplines/test-environment-management/test-environment-management-standards.md)
  - [Test Environment Monitoring Standards](../disciplines/test-environment-management/test-environment-monitoring-standards.md)

- **Checklists**
  - [Release Compliance Controls — Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)