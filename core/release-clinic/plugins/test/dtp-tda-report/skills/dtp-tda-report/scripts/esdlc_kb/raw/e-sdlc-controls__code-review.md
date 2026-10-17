# Controls: Code Review

---

## Control Attributes

| **Control Name** | Code Review |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Minimize the risk of code errors by identifying specific design and coding-practice related flaws that could impair system security, integration, stability and maintainability. |
| **Control Requirements** |<br/>- All Code must undergo code quality scanning and must not contain any major vulnerabilities, breaches to coding standards.<br/>- Solution Components are acquired or created as per agreed code quality requirements and thresholds before merge or integration with other code or components.<br/>- Adopt to automated code review tools wherever possible<br/>- Vendor solutions are confirmed to have met required quality standards. |
| **Control Tasks** | For Bespoke applications<br/>1.Perform Static Code & Security Code analysis for all incremental code changes/inclusions.<br/>- Ensure that source code adheres to agreed coding standards and passes the associated quality and security (AIVM) assessments.<br/>- Ensure that all code changes are reviewed to prevent errors in the code from being merged into the release candidate.<br/>- Manage Code Quality as per the defined threshold.<br/>2. Adopt automated code review tools wherever possible<br/>- In case of unsupported code establish peer review mechanism following the coding standards. For Vendor solutions<br/>- Establish contractual commitments from the Vendors on all the deliverables for meeting the required quality standards.<br/>- Gather evidence for adherence ahead of integration or acceptance. For all the code related changes:<br/>- Ensure peer-based code review are conducted to prevent Functional code anomalies.<br/>- Code review report must be attested as part of the release. Note:<br/>- For SCB developed code and where source code is provided to the bank for integration: Control Tasks must be carried out using the Banks standard processes and tools For More guidelines on code review, refer:<br/>- [Code Quality Review Handbook](../guidance/all-guidelines/code-quality-review-handbook.md)<br/>- [Code Quality and Code Security Guidelines](../guidance/all-guidelines/code-quality-and-code-security-guidelines.md) |
| **Evidence** | The controls expectations must be met using the Banks standard process & tools. Evidence are accumulated automatically if using the bank's engineering pipeline. |

| Sl.No | What | When | Scope | Approver | Document Update/Review Frequency | **Evidence - ADO** |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | - **Automated**: Report from Sonarqube or Equivalent tool.<br/>- **Manual**: Code review performed as a part of pull request approval<br/>- **For Binaries:** Vendor attestation. | Construction | Adherence to the code Quality standards | Engineering Lead | New Build | **For Bespoke Applications:** Code scan report evidenced automatically if using E-SDLC prescribed Quality gates in SonarQube. For code that is not compatible with SonarQube, the code review must be performed as part of the Pull Request by the Engineering Lead.<br/><br/>For Vendor delivered applications<br/>- Vendor’s attestation confirming that code review has been conducted and code quality defects are resolved before being shipped to SCB.<br/>- Evidence must be produced for all the binaries/releases delivered when required.<br/>- Vendor's methodologies showing practices are in line with industry standards specific to software development (e.g. ISO or CMMi) to demonstrate code review is part of the process |  |  |  |  | . |
| 2 | Vulnerability Scan results | Construction | To ensure code is free from Security vulnerabilities | Engineering Lead | New Build | Code security scan report evidenced in the engineering pipeline.<br/><br/>**For Vendor delivered applications**<br/>- Vendor’s attestation confirming that vulnerability scan has been conducted and any known vulnerabilities are resolved before being shipped to SCB.<br/>- Evidence must be produced for all the binaries/releases delivered when required.<br/>- Vendor's methodologies showing practices are in line with industry standards specific to vulnerability management to demonstrate vulnerability scan is part of the process. |  |  |  |  |  |

## Relationships

### Content References

- [Code Quality and Code Coverage Metrics](../guidance/supporting-materials/code-quality-and-code-coverage-metrics.md)


### Qualified References
- **Disciplines**
  - [Implementation](../disciplines/implementation.md)
- **Tasks**
  - [Conduct Code Review](../disciplines/implementation/conduct-code-review.md)
  - [Set up Tools - Development](../disciplines/governance-and-tooling/set-up-tools-development.md)
- **Artifacts**
  - [Code Quality Review Report](../work-products/implementation/code-quality-review-report.md)
- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [SonarQube](../appendix/reference/sonarqube.md)
  - [About pull requests](../tools/next-gen-pipeline-ado/about-pull-requests.md)
  - [Next Gen Pipeline- ADO - General FAQ](../tools/next-gen-pipeline-ado/next-gen-pipeline-ado-general-faq.md)
  - [How to create a new Git branch](../tools/next-gen-pipeline-ado/how-to-create-a-new-git-branch.md)
  - [Understanding of ADO RBAC](../tools/next-gen-pipeline-ado/understanding-of-ado-rbac.md)
  - [Understanding of E-SDLC-Unit Testing, Code Quality & SAST](../tools/next-gen-pipeline-ado/understanding-of-e-sdlc-unit-testing-code-quality.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [Vx ESDLC Control - Code Quality Review Completed](../appendix/guidance/vx-esdlc-control-code-quality-review-completed.md)
  - [What is Azure Repos?](../tools/next-gen-pipeline-ado/what-is-azure-repos.md)
- **Templates**
  - [Code Review Report Template](../templates/code-review-report-template.md)
- **Guidelines**
  - [Behavior-Driven Development Guidelines](../guidance/guidelines-by-discipline/development/behavior-driven-development-guidelines.md)
  - [Test-Driven Development Guidelines](../guidance/guidelines-by-discipline/development/test-driven-development-guidelines.md)
  - [Code Quality and Code Security Guidelines](../guidance/all-guidelines/code-quality-and-code-security-guidelines.md)
  - [Code Quality Review : Handbook](../guidance/all-guidelines/code-quality-review-handbook.md)
  - [Application Code Analysis](../guidance/all-guidelines/application-code-analysis.md)
  - [Source Code](../guidance/all-guidelines/source-code.md)
  - [ICS Security Standards](../guidance/supporting-materials/ics-security-standards.md)
  - [Code Security Review Guidelines](../guidance/all-guidelines/code-security-review-guidelines.md)
  - [AIVM Pattern: Vulnerability Management - Code Review](../guidance/all-guidelines/aivm-pattern-vulnerability-management-code-review.md)
- **Metrics and Measurements**
  - [Vx ESDLC Control - Code Quality Review Completed](../appendix/guidance/vx-esdlc-control-code-quality-review-completed.md)
- **Checklists**
  - [Release Compliance Controls — Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)