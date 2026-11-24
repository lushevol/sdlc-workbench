# Controls: Software Configuration Management

---

## Control Attributes

| **Control Name** | Software Configuration Management |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Ensure all software assets (source code, binaries, installation / configuration scripts and files) are identified and available under Software Configuration Management.<br/>- Protect the Bank's applications from loss of source code or configuration.<br/>- Enable releases running in Production to be retrieved from SCM repositories when required.<br/>- Protect the integrity of the release for all code changes and prevent unauthorized changes. |
| **Control Requirements** |<br/>- All repositories that are used to store code or configuration items for the Banks' applications must be tagged to the Application ID to ensure traceability.<br/>- Binaries must only be stored in the Banks approved Artifactory repository.<br/>- For source code and configuration, only the Bank's standard repositories are used. Refer [Standard Source code and Binary Repositories](../disciplines/software-configuration-management/standard-source-code-and-binary-repositories.md)<br/>- Ensure deployment to production only stems from approved repositories (Covers internal / Third party / vendor / external binaries / dependencies (shared libraries))<br/>- Ensure User activities are logged with unique user identifier in authorized repository.<br/>- Access control (& segregation of duties) at source code level to prevent unauthorized changes.<br/>- Ensure Unique identifier is applied to each build with proper versioning and truthful metadata.<br/>- Protect the integrity of production deployments by ensuring no change is introduced to deployable package after its been tested and approved. |
| **Control Tasks** |<br/>- Configure code repositories to ensure:<br/>&emsp;- Only standard branching patterns are applied<br/>&emsp;- Separation of duties for Maker and Checker on pull request<br/>&emsp;- All code and configuration changes are tagged to the relevant requirement ID<br/>&emsp;- All code received from vendors is merged into the build via pull request process<br/>- Configure binary repositories to ensure:<br/>&emsp;- Each production release (binaries, config, deployment scripts etc) to be identified via a unique, immutable reference.<br/>&emsp;- Only use approved Third-Party technology products (binary products, source code, libraries, etc).<br/>- Ensure no sensitive information (e.g. secrets, customer data) are stored in code repositories. Refer [PID - IAM Pattern: Access Management - Privileged ID Vaulting (IAM-2)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=774312958)<br/>- Ensure all the relevant checks prior to consuming Third-party/vendor binaries/OSS/OSL or creating repositories for applications are completed. Refer [Artifact Ingestion Procedure](https://confluence.global.standardchartered.com/x/k4_Gtw) |
| **Evidence** | The controls expectations must be met using the Banks standard process & tools. Evidence is accumulated automatically if using the bank's engineering pipeline. |

| **Sl.No** | **Evidence** | **When** | **Standard repositories** | **Performer** | **Approver** | **Document Update/Review Frequency** | **Evidences** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NA | All Phases | ADO Repos; Endeavor (Mainframe) | Automatic | Automatic | Live | **ADO**: Evidence is accumulated automatically in the engineering pipeline. |

## Relationships

### Qualified References

- **Disciplines**
  - [Software Configuration Management](../disciplines/software-configuration-management.md)

- **Tasks**
  - [Setup Software Configuration Repositories](../disciplines/software-configuration-management/setup-software-configuration-repositories.md)
  - [Approve Code and Configuration Changes](../disciplines/software-configuration-management/approve-code-and-configuration-changes.md)
  - [Retrieve Production Release](../disciplines/software-configuration-management/retrieve-production-release.md)
  - [Establish Software Configuration Management (SCM) Plan](../disciplines/software-configuration-management/establish-software-configuration-management-scm.md)

- **Artifacts**
  - [Software Configuration Management Plan](../work-products/configuration-and-change-management/software-configuration-management-plan.md)

- **Tools**
  - [About pull requests](../tools/next-gen-pipeline-ado/about-pull-requests.md)
  - [How To - Create a dashboard in Azure Devops?](../tools/next-gen-pipeline-ado/how-to-create-a-dashboard-in-azure-devops.md)
  - [How To - Create a query in Azure Boards?](../tools/next-gen-pipeline-ado/how-to-create-a-query-in-azure-boards.md)
  - [How to create a new Git branch](../tools/next-gen-pipeline-ado/how-to-create-a-new-git-branch.md)
  - [Know more about User Access](../tools/next-gen-pipeline-ado/know-more-about-user-access.md)
  - [Understanding of ADO RBAC](../tools/next-gen-pipeline-ado/understanding-of-ado-rbac.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [What is a group in Azure Devops?](../tools/next-gen-pipeline-ado/what-is-a-group-in-azure-devops.md)
  - [What is Azure Repos?](../tools/next-gen-pipeline-ado/what-is-azure-repos.md)
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Branching Strategy](../appendix/guidance/branching-strategy.md)

- **Guidelines**
  - [Software Configuration Management Guidelines](../disciplines/software-configuration-management/software-configuration-management-guidelines.md)
  - [Software Configuration Management Standards](../disciplines/test-environment-management/software-configuration-management-standards.md)
  - [Continuous Delivery Guidelines](../guidance/guidelines-by-discipline/implementation/continuous-delivery-guidelines.md)
  - [Continuous Integration Guidelines](../guidance/guidelines-by-discipline/implementation/continuous-integration-guidelines.md)
  - [RBAC User Guide](../guidance/supporting-materials/rbac-user-guide.md)
  - [Standard Source code and Binary Repositories](../disciplines/software-configuration-management/standard-source-code-and-binary-repositories.md)
  - [ADO Source Code Repository](../guidance/all-guidelines/ado-source-code-repository.md)

- **Checklists**
  - [Release Compliance Controls â€” Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)