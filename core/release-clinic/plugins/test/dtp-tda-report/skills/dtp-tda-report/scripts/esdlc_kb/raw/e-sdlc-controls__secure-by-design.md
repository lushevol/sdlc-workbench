# Controls: Secure by Design

---

## Control Attributes

| **Control Name** | Secure by design |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Solutions are assessed for the security impact. |
| **Control Requirements** |<br/>- Perform Threat model and determine the potential threats for all the new Applications/Infra/products/change.<br/>- Perform Threat model for all the new projects or whenever there is an architecture change.<br/>- Determine Minimum Security Baseline Requirements to ensure that security threats are addressed as a part of Design and Architecture review.<br/>- Determine the implementation procedure for the identified security baseline controls.<br/>- Design TIP for any new Infrastructure, product and applications before Production.<br/>- Ensure Scanning and other related policies are assigned, validated.<br/>- Ensure security coding best practices are followed. Vulnerabilities are identified and remediated or exception recorded.<br/>- Adopt standards Security tools and Integrations.<br/>- Security testing's are conducted ahead of production release.<br/>- Ensure security risks are assessed as part of the Pre-deployment verification and exceptions are tracked as per security dispensation process.<br/>- All the security non compliances are raised in the Non-Compliance management system. |
| **Control Tasks** |<br/>- For any initiative / proposed change:<br/>1. Perform Threat model for all new projects or whenever there is an architecture change.<br/>2. Determine Minimum Security baseline (control) requirements based on the threats identified as per the ICS standards.<br/>3. Determine the implementation procedure for the identified security baseline controls.<br/>&emsp;3.1. Design TIP for any new Infrastructure components before Production. [TIP User Guide](https://confluence.global.standardchartered.com/display/SDF/TIP+User+Guide)<br/>For Software:<br/>1. Ensure security coding best practices are followed. Vulnerabilities are identified and remediated.<br/>2. Perform Vulnerability Testing<br/>3. Perform Penetration testing<br/>For Infrastructure:<br/>1. Perform SAT. More information on SAT: [SAT - Infrastructure Vulnerability Scanning](https://confluence.global.standardchartered.com/display/SDF/Copy+of+SAT-Infrastructure+Vulnerability+Scanning)<br/>&emsp;- [Infrastructure Vulnerability Scanning SRM Guideline](https://confluence.global.standardchartered.com/display/AIVM/SRM+guideline+for+Ad-Hoc+Infrastructure+Vulnerability+Scan+Request)<br/>Notes:<br/>- Backlog of security controls to be implemented and prioritized as part of NFR.<br/>- All the non-compliances must be reported and managed in NCR.<br/>- All the release level non-compliances raised as part of the build are evaluated (false positive) and fixed or deferred to later date with approval from CISO. |
| **Evidences** | The controls expectations must be met using the Banks standard process & tools. Evidences are accumulated automatically if using the bank's engineering pipeline, any other approach requires manual evidencing in the pipeline. |
| **Guidance Materials** | Kindly refer the References under Relationship section |

| Evidences | When | Scope | Performer | Approver | Document Update/Review Frequency | Evidence - ADO |
| --- | --- | --- | --- | --- | --- | --- |
| Security Requirements | Design | A set of security requirements to protect an Information System or a Technology Infrastructure | Engineering Lead | Domain Architect approves the sTK during the ARF / DTC forum which ever is the SI Chapter 3 approval authority. ESA approval is implicit in the ARF / DTC approval itself. | sTK must be updated if: New applications<br/>- Every applications within the Group must have Security Architecture established System level attributes (example SBIA rating) changes, One or more components are added or removed, or their attributes (reference the columns in the sTK Application Design Technology Details table), One or more connectivity are added or removed, or changed their attributes (reference the columns in the sTK Application Design Connectivity Details table), or with Major sTK version releases | Link to detailed design under the Detailed Design tab in SI work item |
| Vulnerability Report | Build |  | Delivery Team | Engineering Lead | Every Release | Automated and available as part of Pipeline report. |

![](/.attachments/fb1634_image2023_4_23_3_38_8.png)

## Relationships

### Content References

- [Design Security Tests For Cloud Infra](../disciplines/all-tasks/design-security-tests-for-cloud-infra.md)


- [Onboarding detective use cases in SIEM](../disciplines/all-tasks/onboarding-detective-use-cases-in-siem.md)


- Guidance
  - [Understanding fastlane for automated security controls](../practices/security-in-delivery/guidance/understanding-fastlane-for-automated-security.md)
  - [Managing hotfix releases](../guidance/all-guidelines/managing-hotfix-releases.md)
  - [SAT Process](../guidance/all-guidelines/sat-process.md)


### Qualified References
- **Tasks**
  - [Commission Security Control Validation](../disciplines/all-tasks/commission-security-control-validation.md)
  - [Design Security Tests](../disciplines/testing/design-security-tests.md)
  - [Execute Security Tests and Produce final report with Sign Off](../disciplines/testing/execute-security-tests-and-produce-final-report.md)
  - [Identify Trigger Points for Engagement](../disciplines/all-tasks/identify-trigger-points-for-engagement.md)
  - [Initiate Security Impact Assessment](../disciplines/design-and-architecture/initiate-security-impact-assessment.md)
  - [Obtain sign-off for adequacy of Security implementation](../disciplines/all-tasks/obtain-sign-off-for-adequacy-of-security.md)
  - [Prepare Minimum Security Baseline Requirements](../disciplines/all-tasks/prepare-minimum-security-baseline-requirements.md)
  - [Identify Trigger Points for Engagement For Cloud Infra](../disciplines/all-tasks/identify-trigger-points-for-engagement-for-cloud.md)
- **Artifacts**
  - [API Technical Specification](../work-products/analysis-amp-design/api-technical-specification.md)
  - [Enhanced Security Requirements](../practices/security-in-delivery/work-products/enhanced-security-requirements.md)
  - [Security Impact Assessment Report](../practices/end-to-end-impact-assessment/work-products/security-impact-assessment-report.md)
  - [Security Risks with Remediation Plans](../practices/security-in-delivery/work-products/security-risks-with-remediation-plans.md)
  - [Test Evidence and Results (Security Tests)](../practices/security-in-delivery/work-products/test-evidence-and-results-security-tests.md)
  - [Test Report (SAT)](../practices/security-in-delivery/work-products/test-report-sat.md)
- **Tools**
  - [Understanding Application Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-application-work-item-in-ado.md)
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [E-SDLC-Checkov ADO Integration - Terraform](../tools/next-gen-pipeline-ado/e-sdlc-checkov-ado-integration-terraform.md)
  - [E-SDLC-Gitleaks](../tools/next-gen-pipeline-ado/e-sdlc-gitleaks.md)
  - [Understanding of E-SDLC-Checkov](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-checkov.md)
  - [Understanding of E-SDLC-Checkov ADO Integration - Kubernetes and Dockerfile](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-checkov-ado-integration.md)
  - [Understanding of E-SDLC-Container Security](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-container-security.md)
  - [Understanding of E-SDLC-Cosign Architecture](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-cosign-architecture.md)
  - [Understanding of E-SDLC-Gitleaks Findings Report](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-gitleaks-findings-report.md)
  - [Understanding of E-SDLC-Gitleaks Functional Testing](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-gitleaks-functional.md)
  - [Understanding of E-SDLC-Gitleaks Policy](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-gitleaks-policy.md)
  - [Understanding of E-SDLC-Gitleaks - Remediation](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-gitleaks-remediation.md)
  - [Understanding of E-SDLC-How to create Whitelisting file](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-how-to-create.md)
  - [Understanding of E-SDLC-Security Work item](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-security-work-item.md)
  - [Understanding of E-SDLC-Sonarqube Quality Gate -Day 0](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-sonarqube-quality-gate.md)
  - [Understanding of E-SDLC-Unit Testing, Code Quality & SAST](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-unit-testing-code-quality.md)
  - [Understanding of E-SDLC-Where to store secret files and credentials?](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-where-to-store-secret.md)
  - [Understanding of E-SDLC-Whitelisting for Gitleaks](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-whitelisting-for-gitleaks.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [Security Impact Assessment (SIA) in Next Gen Pipeline - ADO](../practices/security-in-delivery/security-impact-assessment-sia-in-next-gen.md)
  - [ICS Non-Compliance Register [ICS NCR]](../practices/security-in-delivery/ics-non-compliance-register-ics-ncr.md)
  - [Solution Intent](../appendix/guidance/solution-intent.md)
- **Guidelines**
  - [API Classifications](../guidance/guidelines-by-discipline/testing/api-classifications.md)
  - [API Guidelines](../guidance/guidelines-by-discipline/testing/api-guidelines.md)
  - [API Testing Guidelines](../guidance/guidelines-by-discipline/testing/api-testing-guidelines.md)
  - [Security Impact Assessment (SIA) Tool User Guide](../guidance/guidelines-by-discipline/analysis-and-design/security-impact-assessment-sia-tool-user-guide.md)
  - [SIA Applicable controls list](../guidance/all-guidelines/sia-applicable-controls-list.md)

- **Checklists**
  - [Release Compliance Controls â€” Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)