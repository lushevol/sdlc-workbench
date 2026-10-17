# Page: E-SDLC Controls

---

## Relationships

### Contents

- [Approved Requirements (Functional & Non-Functional)](e-sdlc-controls/approved-requirements-(functional-and-non_functional).md)
- [Architecture and Design Sign-off](e-sdlc-controls/architecture-and-design-sign-off.md)
- [Software Configuration Management](e-sdlc-controls/software-configuration-management.md)
- [Test Environment Management](e-sdlc-controls/test-environment-management.md)
- [Code Review](e-sdlc-controls/code-review.md)
- [Unit Testing](e-sdlc-controls/unit-testing.md)
- [Test Strategy](e-sdlc-controls/test-strategy.md)
- [Secure by Design](e-sdlc-controls/secure-by-design.md)
- [Functional Testing](e-sdlc-controls/functional-testing.md)
- [Non Functional Testing](e-sdlc-controls/non-functional-testing.md)
- [Pre-Deployment verification](e-sdlc-controls/pre-deployment-verification.md)
- [Post Deployment Verification](e-sdlc-controls/post-deployment-verification.md)
- [E-SDLC Integrated Training](e-sdlc-controls/e-sdlc-integrated-training.md)
- [Data](e-sdlc-controls/data.md)

## Main Description

**E-SDLC Mandatory Controls**

Adherence to all E-SDLC controls is mandatory for all Technology Delivery Initiatives and Releases (Applications and Infrastructure alike). Non-adherence to the E-SDLC controls may lead to regulatory/audit actions, direct/in-direct impact to the application maintainability and stability.

| Control Name | Control Trigger | Control Implementation in ADO | Control Type | Control Applicability | SDF Controls (to be retired effective from the date of ESDLC launch. *Note: SIA control will be still retained in ESDLC*) |
|---|---|---|---|---|---|
| [Approved Requirements (Functional & Non-Functional)](e-sdlc-controls/approved-requirements-(functional-and-non_functional).md) | Release | Automated | Preventive | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | Business Requirements (Functional) Approved<br>Business Requirements (Non-Functional) Approved |
| [Architecture and Design Sign-off](e-sdlc-controls/architecture-and-design-sign-off.md) | Application | Partially Automated | Preventive | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | Solution Intent Signed-off (formerly known as HL Architecture Sign-off) |
| [Software Configuration Management](e-sdlc-controls/software-configuration-management.md) | Platform | Automated | Preventive | Source Codes<br>Configurations<br>Open-Source Software /libraries<br>Containers | Standard SCM repositories used<br>Code and Config Change Approved<br>Production Release can be Retrieved |
| [Test Environment Management](e-sdlc-controls/test-environment-management.md) | Platform | Automated | Preventive | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | Test Environment Controlled<br>Test Environment Monitoring and Configuration Tracked<br>Test Environment Specification Signed-off |
| [Code Review](e-sdlc-controls/code-review.md) | Release | Automated | Preventive | Software-Bespoke<br>Software – Vendor deliveries | Code Quality Review Completed |
| [Unit Testing](e-sdlc-controls/unit-testing.md) | Release | Automated | Preventive | Software-Bespoke | Unit Testing Completed |
| [Test Strategy](e-sdlc-controls/test-strategy.md) | Application | Partially Automated | Preventive | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | Test Strategy Signed-Off |
| [Secure by Design](e-sdlc-controls/secure-by-design.md) | Release | Partially Automated | Detective | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | SIA: Security Control Verified and Signed-off |
| [Functional Testing](e-sdlc-controls/functional-testing.md) | Release | Automated | Preventive | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | Test Evidence Traceability Report Maintained<br>Test Closure Report Signed-Off |
| [Non-Functional Testing](e-sdlc-controls/non-functional-testing.md) | Application | Partially Automated | Detective | Software Deliveries<br>Cloud – SAAS/IAAS/PAAS | Application Performance and Stability Testing<br>Release Performance and Stability Testing |
| [Pre-Deployment verification](e-sdlc-controls/pre-deployment-verification.md) | Release | Automated | Preventive | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | Release Integrity Verified<br>Operations Manual Signed-Off<br>Technical Deployability Confirmed |
| [Post Deployment Verification](e-sdlc-controls/post-deployment-verification.md) | Release | Automated | Detective | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | None |
| [E-SDLC Integrated Training](e-sdlc-controls/e-sdlc-integrated-training.md) | Squad | Automated | Preventive | Software Deliveries<br>Infrastructure – On prem<br>Cloud – SAAS/IAAS/PAAS | None |
| [Data](e-sdlc-controls/data.md) | Release | Partially Automated | Preventive | Software Deliveries<br>Cloud – SAAS/IAAS/PAAS | None |

**Note:** All E-SDLC submitted artefacts must capture relevant data as per template. However, approval/sign off party is accountable for validating all the required information are captured in the submitted artefacts. After signoff, it is implicit that left out information is considered not applicable. For more information on Role Based Access Control, refer to [RBAC User Guide](guidance/supporting-materials/rbac-user-guide.md)

For more information on Role Based Access Control, refer to [RBAC User Guide](rbac-user-guide.md)

### Checklists

- [Release Compliance Controls — Pre-Flight Checklist](checklist/compliance-checks-preflight-checklist.md)