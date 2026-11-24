# Controls: Pre-Deployment verification

---

## Control Attributes

| **Control Name** | Pre-Deployment Verification |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Standardized deployment strategies are adopted.<br/>- Determine all the release components are rightly identified and tagged with a unique release version ID.<br/>- Determine all the required testing (Functional, Non-Functional, Security validations) are completed successful before deploying into production. |
| **Control Requirements** |<br/>- Perform Pre-deployment checks (For all the deployments to non prod and prod). Ensure releases - are technically deployable - have dependencies documented - have known bugs (with possible workarounds) documented - have included capabilities documented - have passed the Testing controls prior to being submitted for deployment to production<br/>- Prod and Non-Prod deployments are automated wherever possible.<br/>- All production deployments must have rollback capabilities or alternative recovery instructions available for the event of unexpected issues during an actual installation.<br/>- All the impacted stakeholders are communicated. |
| **Control Tasks** |<br/>- Ensure the release impact assessment performed on the scope and all the appropriate risks are identified, fixed or mitigated.<br/>- Ensure deployment approach is agreed before commencement.<br/>- Ensure all changes (commits) included in the release candidate are traced to an approved in-scope requirement for the release. For each change committed to the release it must reference the requirement ID related to the change.<br/>- Ensure deployment scripts are version controlled, stored in the standard repository associated with the application and are successfully tested.<br/>- Ensure all the Security, and Technology related (Configuration, Testing) compliance checks are completed, and exceptions are accepted and tracked.<br/>- For releases with automated deployment<br/>1. Develop and test installation (deployment) scripts with - ability to automate the installation. - ability to determine whether entry condition for an installation are met - ability to detect whether an installation resulted in an expected target state of the environment.<br/>- For releases which require manual deployment<br/>1. Develop and test installation (deployment) guide with - detailed installation instructions - detailed instructions to determine whether entry condition for an installation are met - detailed instructions on how to verify whether an installation resulted in an expected target state of the environment<br/>- Technology services support teams are informed/updated on the housekeeping tasks required to run the application in production.<br/>- Ensure that the following operational activities are identified and planned:<br/>1. Automated Archiving and Housekeeping<br/>2. Application Monitoring and Alerting<br/>3. Application batch jobs are defined in CTRL-M<br/>- Ensure system run manual is in place for infrastructure.<br/>- Establish formal release notes covering<br/>1. Capabilities included with this release (prior and incremental)<br/>2. Conditions under which acceptance was achieved (e.g. level of load testing passed and what performance to expected under what kind of configuration)<br/>3. Pre-requisites (dependencies) that must be met for a successful deployment of the release (e.g. versions of underlying OS etc) |
| **Evidence** | The controls expectations must be met using the Banks standard process & tools. Evidences are accumulated automatically if using the bank's engineering pipeline, any other approach requires manual evidencing and would be treated as Risk sensitive. **Note** : AIG and Operation Manual must be reviewed at least on a yearly basis by the approval parties if there is no planned changes in that document in the recent 1 year and ensure reviewed version is available |

| **Sl.No** | **Deployment Type** | **Evidence** | **When** | **Scope** | **Performer** | **Approver** | **Document Update/Review Frequency** | **Evidence<br/>- ADO** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Application/ Software/ Containers/Data/Binaries/Infra | AIG inclusive of Scripts and Installation & Rollback procedure | Transition | Technical deployment | Delivery Team | Engineering Lead/Delegate | Before deployment | For automated deployment: **AIG:** No explicit AIG doc needs to be provided for automated deployment under Release work item<br/>- Release control tab **Rollback:**<br/>- No explicit roll back script / document required if the automated rollback stage is configured in pipeline<br/>- If no automated rollback stage is configured in pipeline, rollback doc (rollback.md) can be evidenced in application repo under main branch or the backout plan section in SNOW CR record captures the Rollback scripts/procedures **For manual deployment:** **AIG and Rollback:** For SaaS/ COTS/ Mainframe Applications: AIG and Roll back document needs to be evidenced in Release work item<br/>- Release control tab. |
| | | ASRM -Operations Manual | Transition | Technical deployment | Delivery Team | Technology Support Manager (PSS) | Before deployment | Operation Manual document needs to be embedded in Application Work item<br/>- Operational Manual Tab |


## Relationships

### Content References

- [How To - Auto Change Record Creation through ADO](../appendix/guidance/how-to-auto-change-record-creation-through-ado.md)


### Qualified References
- **Disciplines**
  - [Deployment](../disciplines/deployment.md)
- **Guidelines**
  - [Bug Management Pipeline Controls User Guide](../guidance/guidelines-by-discipline/testing/Bug-Management-Pipeline-Controls-User-Guide.md)
- **Tasks**
  - [Conduct Deployment Impact Assessment](../disciplines/deployment/conduct-deployment-impact-assessment.md)
  - [Define Deployment Strategy](../disciplines/deployment/define-deployment-strategy.md)
  - [Develop Deployment script and configuration](../disciplines/deployment/develop-deployment-script-and-configuration.md)
  - [Develop Installation Work Products](../disciplines/all-tasks/develop-installation-work-products.md)
  - [Perform Release Test](../disciplines/release-management/perform-release-test.md)
  - [Perform Test Environment Monitoring](../disciplines/test-environment-management/perform-test-environment-monitoring.md)
  - [Prepare Operations Artifacts](../disciplines/all-tasks/prepare-operations-artifacts.md)
  - [Sign-off on Operations Artifacts](../disciplines/all-tasks/sign-off-on-operations-artifacts.md)
  - [Track Test Environment Configuration](../disciplines/test-environment-management/track-test-environment-configuration.md)
  - [Verify and Obtain sign-off on Installation Work Products](../disciplines/software-configuration-management/verify-and-obtain-sign-off-on-installation-work.md)
  - [Verify the Release Integrity](../disciplines/software-configuration-management/verify-the-release-integrity.md)
- **Artifacts**
  - [[Operations Artifacts]](../work-products/operations-amp-support/operations-artifacts.md)
  - [Application Installation Guide (AIG)](../work-products/operations-amp-support/application-installation-guide-aig.md)
  - [Deployment Strategy](../work-products/deployment/deployment-strategy.md)
  - [Installation scripts](../work-products/operations-amp-support/installation-scripts.md)
  - [Release Package](../work-products/release-management/release-package.md)
  - [Release Plan](../work-products/release-management/release-plan.md)
  - [Release Strategy](../work-products/release-management/release-strategy.md)
  - [Traceability Report](../work-products/testing/traceability-report.md)
- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Understanding Application Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-application-work-item-in-ado.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [Managing a Release Work Item with multiple Change Requests](../tools/Managing-a-release-work-item-with-multiple-Change-Requests.md)
- **Templates**
  - [ASRM - SCB](../templates/asrm-scb.md)
  - [Application Installation Guide (AIG)](../templates/application-installation-guide-aig.md)
- **Guidelines**
  - [Enterprise Monitoring Guidelines](../guidance/guidelines-by-discipline/operations-amp-support/enterprise-monitoring-guidelines.md)
  - [Test Environment Monitoring Standards](../disciplines/test-environment-management/test-environment-monitoring-standards.md)
  - [Release Impact Assessment for Production Releases](../guidance/guidelines-by-discipline/configuration-and-change-management/release-impact-assessment-for-production-releases.md)

- **Checklists**
  - [Release Compliance Controls â€” Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)