## **BPMS New Feature Onboarding Operational Readiness Questionnaire**

## 1. Business Context & Scope

*Define the business value, user base, and basic flow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **VAT Approval** | - VAT approval obtained. | **- VAT** **Approval:** [VAT Request - SSI+: Dormant SSI Setup and Closures - Financial Markets Virtual Architecture Team - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3739155851) |
| **Functionality Description** | - Briefly describe the functionality to be built for the flow. | **- Functionality:** Provide an API that allows SSI+ to access daily incremental data on the SSIs that have been used, which covers both BCS and FMPR flows. |
| **Current Business Handling** | - Existing Flow: How are this business currently handled? - New Interface: Respond as "New Interface". | - **Existing Flow:** It will pass different parameters in existing API /v2/data/provider/query/cashflows - **New Interface:** [New Interface] Create new API to query BCS SSI daily usage |
| **End-to-End Flow** | - Provide End-to-End Flow Diagram. - Include data flow, process/DB SP, sample message, E2E impact. | - **Diagram:** `[Diagram Link]`. - **Details:** [Dormant SSI processing - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Dormant+SSI+processing) Existing API: SSI PLUS → RATAN-CASH-SETTLEMENT-QUERY-SERVICE New API: SSI PLUS → RATANONE-STAMPING-SERVICE |
| **Scope (Country/Product)** | - Rollout Country/Entity? - Product/Asset Class involved? | - **Country/Entity: **N/A - **Product/Asset:** N/A |
| **Clients & Users** | - Client Type (Internal, External, Regulatory)? - Number of users introduced? - User location? | - **Client Type:** Internal Operations - **User Count:** Service account - **User ****Location:** N/A |
| **Volume & Business Hours** | - Daily Volume & Peak Volume? - Business Hours & Peak Hour? | **- Volume:** Common API: 10K records BCS API: 1K records **- frequency:** 1 time/day (Tue-Sat) 2 time/day (Mon) - **Business** **Hours:** 00:55 GMT - **Peak Hour:** N/A |
| **Support Hours** | - Expected support hours defined (e.g., 8*5, 24*5). - BAU model defined for **Static Data, Interface Control, Monitoring, Alerting, Tracking, Reporting, License/key renew, Restart/Reboot/Patching.** | - **Hours:** 8x5 - **BAU Model:** |
| **Release Plan** | - Release frequency (Single, Half-yearly, Quarterly, Monthly, Weekly) and planned upgrade schedule. | - **Release ****Frequency:** Single - **Next Upgrade:** N/A |
| **Tech Stack & Infrastructure** | - New Technology Stack involved? - New Infrastructure (Server, Hardware, Network)? - Provide Architecture Diagram. | - **Stack:** N/A - **Infra:** N/A - **Diagram: **N/A |
| **Vendor Management** | - If vendor product is used: Share contract details (contract, ER, renewal date, vendor contact) and issue raising procedure. | - **Vendor:** N/A - **Contract:** N/A |

---

## 2. Architecture & System Onboarding

*Assess technical implementation, interface standards, and system registration.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Interfaces & Data Feeds** | - What are the interfaces and data face to be introduced? - Interface Type (Real-time, Batch, etc.)? - If Batch: How many data feeds? Provide details. | - **Interfaces:** Downstream API - **Type:** Real Time - **Batch Count: **N/A |
| **System Registration** | - App onboarded in **CMDB**. - App ready in **ServiceNow**. - App ready in **ADO** (Azure DevOps). | - **CMDB:** Yes - ID: Ratan-51358 - **ServiceNow:** Yes - ID: Ratan-51358 - **ADO:** Yes - Project: FMQPR-51358 |
| **Naming Conventions** | - Application code/package folder naming follows standard. - Control-M Job/Smartfolder naming follows standard. - Inbound/Outbound folder/path naming follows standard. | - **Code Naming:** N/A - **Control-M:** N/A - **Folders:** N/A |

---

## 3. Operational Resilience & Exception Handling

*Core operational requirements. **Test evidence must be provided for each checkpoint.**.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **E2E Flow Control** | - Ensure successful message delivery. - Raise exception to responsible team on time. - ACK/NACK mechanism or E2E reconciliation in place. - Validation on Completeness & Accuracy. | - **Delivery:** Guaranteed via API response. - **Exception:** Check error log - **ACK/NACK:** N/A - **Validation:** Checksum & Record Count Validation |
| **Auto Resume (Connectivity)** | - Auto resume connectivity (continuously re-try mechanism) with upstream/downstream/middleware. - **No manual intervention required.** | - **Auto Resume: **N/A -** ****Manual Intervention: ** N/A |
| **Infrastructure Issue Handling** | - Able to stop process in case of infra issue (DB, Unix, Network, TDE). - Resume process automatically without data loss/partial processing once resolved. | - **Stop Process: **N/A - **Auto Resume:** N/A |
| **Single Message Failure** | - Able to handle single message failure automatically without stopping/suspending application process. | - **Handling:** N/A - **Process Status:** N/A |
| **DB Transaction Management** | - Done properly to ensure system can be gracefully shutdown without any message stuck, lost, or partially processed. | - **Transaction:** N/A - **Shutdown:** N/A |
| **Exception Categorization** | - Properly categorize exception type (Technical vs. Data). - Auto recover technical issues (e.g., infra outage). - Route data issues to responsible team. | - **Exception** **Categorization:** Follow RATAN current process - **Auto Recover:** Follow RATAN current process - **Data Issues:** Follow RATAN current process |
| **DR Configuration** | - Both Production and DR sites configured without single point of failure. - No configuration change required for DR switchover. | - **DR Sites:** Follow RATAN current process - **Switchover:** Follow RATAN current process |
| **File Handling** | - In case of file download failure, able to re-download automatically without manual intervention. | - **Re-download:** N/A - **Manual Intervention:** N/A |
| **Database Health** | - Ensure no bad execution plan introduced for new SQL/SP. - Ensure no invalid DB objects introduced by DB change. | - **Execution Plan:** SQL Reviewed & Optimized in Dev stage - **DB Objects:** All Objects Validated Post-Deploy |
| **Automatic Housekeeping** | - Automatic housekeeping in-place (Files, DB, Temp, Logs, Inbound/Outbound). - If missing, CRISP to cover with remediation plan. - **ASRM Details:** Job name, Frequency, Target details. | - **Housekeeping:** N/A - **CRISP:** N/A - **ASRM:** N/A |
| **Manual Tasks** | - **No manual tasks** will be introduced by this release. | - **Manual Tasks:** `Zero Manual Tasks for BAU` |
| **Logging** | - Logging in place with proper level (INFO, WARN, ERROR). - Details stated in ASRM. - Standardized service log pattern for monitoring tool capture. | - **Levels:** `INFO, WARN, ERROR Configured` - **ASRM:** `Details Included in ASRM` - **Pattern:** JSON Format for Splunk Ingestion |
| **Holiday & Greenzone** | - Proper agreement on Holiday cases (auto handling). - Job schedules avoid Greenzone window. - Green Zone agreed in OLA/SLA for weekend activities. | - **Holiday:** N/A - **Greenzone:** N/A - **OLA/SLA:** N/A |

---

## 4. Automation & Deployment

*Automation is mandatory to reduce operational risk.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Service Control** | - One-click stop/start of all services & single service. | - **Control:** `Scripts Available in ADO for Full/Single Service` |
| **Deployment** | - **One-click deployment using ADO pipeline.** - Any other method requires dispensation approval. | - **Deployment:** `CI/CD Pipeline Configured in ADO` - **Other Method:** `None Used` |
| **Disaster Recovery** | - **One-click DR** switchover. | - **Switchover:** `Button Available in Control Dashboard` |
| **Server Maintenance** | - Server patching via ADO pipeline (auto maintenance window). - Auto Server reboot (via CR if touch token not used). | - **Patching:** `Automated via Ansible/ADO` - **Reboot:** `Automated via Change Request` |
| **Fully Automated Operations** | - Automated restart, deployment, DR, and housekeeping. | - **Operations:** `All Key Operations Automated` |

---

## 5. Monitoring & Alerting

*Ensure production visibility and proactive alerting.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Application Status** | - Health check/status monitor from **ITRS** for all components/services/API/GUI. | - **ITRS Probe:** `Deployed for all components` - **Coverage:** `Services, API, GUI monitored` |
| **Interface Connectivity** | - All real-time interface connectivity health check. - Batch file receiving/sending monitoring. - Batch processing monitoring. | - **Real-time:** `Checks active via Heartbeat` - **Batch File:** `Monitors active for In/Out` - **Processing:** `Latency monitored per job` |
| **Infrastructure Monitoring** | - Infra connectivity (DB, Solace, MQ, OUD, MFA, Kafka, Redis, etc.). - Network, Disk space, Filesystem. - DB space, long running query, blocking session, active session count. | - **Connectivity:** `All components monitored (DB, MQ, Kafka)` - **Infra:** `Disk/Network alerts configured` - **DB Health:** `Space, Queries, Sessions active` |
| **Capacity Monitoring** | - CPU/Memory utilization < 70%. (for active-passive, if it's active-active cluster then 2 nodes added together <70%). - Disk/DB space utilization < 70% ((for active-passive, if it's active-active cluster then 2 nodes added together <70%).) - Trade volume monitoring (Hourly/Daily/Weekly). | - **CPU/Mem:** `Threshold set at 70%` - **Disk/DB:** `Threshold set at 70%` - **Volume:** `Trade Volume monitor configured` |
| **Transaction Monitoring** | - All messages processed as expected. - Detect abnormal trade processing or stuck trades in intermediate status. - MQ/Kafka pending message queue monitoring. | - **Messages:** `Transaction logs monitored` - **Stuck Trades:** `Alerts configured for intermediate status` - **Queue:** `MQ/Kafka Queue depth monitored` |
| **Performance & SLA/OLA** | - Processing throughput and latency monitoring. - Key deliveries meet SLA requirements. - Meet expected cutoff following OLA. | - **Performance:** `Throughput/Latency monitor available` - **SLA:** `SLA metrics tracked` - **OLA:** `Cutoff alerts enabled` |
| **Certificates** | - Expiry day monitor for all in-use certificates/licenses. | - **Monitor:** `Certificate expiry alert set (30 days prior)` |

---

## 6. Support Model & Access Management

*Define who supports the app and how access is controlled.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Vaulting & Accounts** | - All prod accounts vaulted (Hashicorp/One-Vault). - PSS Read-only accounts ready (DB, Server, Software) before Go-Live. - Security Matrix ready. | - **Vaulting:** `Secrets vaulted in Hashicorp` - **Accounts:** `Read-only accounts created` - **Matrix:** `Security Matrix ready]` |
| **File Access** | - All files (config, inbound, outbound, logs) viewable by PSS read-only accounts. **No 777 access** to prod files. | - **Permissions:** `Confirmed: Permissions set to 640` - **Access:** `PSS has read access` - **Security:** `No 777 access found` |
| **ITRS Privilege** | - ITRS interactive privilege ID to STOP & START the ITRS netprobe process. | - **ID Provided:** `ITRS_ID_123` |
| **User Access Management** | - Centralized management by OneCert. - Access request automated via SRM (UAM/IAM, ULA, URA). - **MFA onboarded** for user authentication. | - **Management:** `OneCert Integrated` - **Automation:** `Access request automated` - **MFA:** `Enabled for all users` |

---

## 7. Documentation & Compliance

*Ensure knowledge transfer and audit compliance. Provide links or attachments.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **OLA (Operational Level Agreement)** | - PSS Manager sign-off. (If OLA is not required, PSS Manager to provide email confirmation) - Developed per OLA template - Uploaded to OLA Central Repository | - **Sign-off:** [Signed off by PSS Manager]. - **Template:** [OLA Template Used]. - **Repository:** [Uploaded to OLA Central Repository] |
| **SLA (Service Level Agreement)** | - BO (Business Owner) sign-off. (If SLA is not required, BO need provide email sign off with justification) - Developed per SLA template. - Uploaded to SLA Central Repository. | - **Sign-off:** [Signed off by BO]. - **Template:** [SLA Template Used]. - **Repository:** [Uploaded to SLA Central Repository] |
| **Capacity Plan (**If capacity plan is not required, TSM to email Capacity Team with justification of why it is not required**)** | - Created in M7 System. - Aligned with FM Capacity Analytics tool. - If not required, TSM to email Capacity Team with justification. | - **System:** [Created in M7]. - **Alignment:** [Aligned with FM Tool] |
| **Service Recovery Plans** | - **Service Recovery Plan:** Developed per template (ITR Process Templates), uploaded to M7. - **Application Restore Plan:** Developed per template, uploaded to SharePoint/M7. | - **SRP:** [Uploaded to M7]. - **ARP:** [Uploaded to M7] |
| **Data Backups** | - Data backups certified in BOARD Portal. | - **Certification:** [Certified]. - **Ref Number:** [Backup-Ref-123] |
| **Test Environment Specification** | - Test Environment Specification completed (Overview, Architecture, Config, Prod vs Test, RAID). - Test Environment Specification template and guide, kindly refer to Appendix | - **Spec:** [Spec Completed, link]. - **Template:** [Template Followed] |
| **ASRM ** | - Data workflow diagram included. - General Troubleshooting guideline (SQL, Log keywords). - Housekeeping details included. - Kindly refer to ASRM template in Appendix | - **Diagram:** [Included]. - **Guidelines:** [Added]. - **Housekeeping: **[Detail provided]. update ASRM “Settlement Flow” chapter： [RATAN ONE Application System Run Manual (ASRM) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3691421338) |
| **Business & Ops Docs** | - BRD (Business Requirements Definition) developed via BRD template. - Operational Runbook / SOP / DOI available. - DASH Onboarding for data extraction. | - **BRD:** [Approved]. - **Runbook:** [Runbook/SOP/DOI Available]. - **DASH:** [Onboarded]. |

---

## 8. Change Management (ServiceNow & AIG)

*Ensure the release process follows change management standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Feature 11933199 [Dormant SSI processing] RATAN Cash Settlement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11933199) |
| **Justification** | - ** Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - ** Issue Fixing:** Provide the issue nature, fix details | Provide an API that allows SSI+ to access daily incremental data on the SSIs that have been used, which covers both BCS and FMPR flows. |
| **Change Test Sign-off** | - Provide evidence link/attachment or N/A with reason 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). UAT Sign-off 5). DR Test Evidence | |
| **UVT plan** | - List details of UVT plan for each story | N/A |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | In CR |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | N/A |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | |
| **Safe Change Attestations** | - Attest or not and Result Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRB Meeting if result is "Not Safe" | |

Appendix:

### Automation

| Purpose | Full URL |
| --- | --- |
| Server Patching (TSP Maintenance Window) | [https://tech.standardchartered.com/tsp/maintenance-window/details/24372](https://tech.standardchartered.com/tsp/maintenance-window/details/24372) |

### Support Documentation

| Purpose | Full URL |
| --- | --- |
| OLA Template | [https://thebridge.zone1.scb.net/docs/DOC-832511](https://thebridge.zone1.scb.net/docs/DOC-832511) |
| OLA Central Repository | [https://teamsites.zone1.scb.net/sites/sm/Pages/OLARepository.aspx](https://teamsites.zone1.scb.net/sites/sm/Pages/OLARepository.aspx) |
| SLA Template | [https://thebridge.zone1.scb.net/docs/DOC-849058](https://thebridge.zone1.scb.net/docs/DOC-849058) |
| SLA Central Repository | [https://teamsites.zone1.scb.net/sites/sm/Pages/SLA.aspx](https://teamsites.zone1.scb.net/sites/sm/Pages/SLA.aspx) |
| M7 System (Capacity Plan Upload) | [https://onepoint.global.standardchartered.com/ui](https://onepoint.global.standardchartered.com/ui) |
| Capacity Analytics Guide | [https://confluence.global.standardchartered.com/pages/viewpage.action?spaceKey=BODSD&title=How+to+use+Capacity+Analytics+to+fill+the+Capacity+Planning+template](https://confluence.global.standardchartered.com/pages/viewpage.action?spaceKey=BODSD&title=How+to+use+Capacity+Analytics+to+fill+the+Capacity+Planning+template) |
| DRP Template (Disaster Recovery Plan) | [https://teamsites.zone1.scb.net/sites/it-resilience/ITR%20Process%20Templates/Disaster%20Recovery%20Plan(Application_Infrastructure).docx?d=wd0b910bfb50c45c195114b38f66d6396](https://teamsites.zone1.scb.net/sites/it-resilience/ITR%20Process%20Templates/Disaster%20Recovery%20Plan(Application_Infrastructure).docx?d=wd0b910bfb50c45c195114b38f66d6396) |
| ITR Process Templates | [https://teamsites.zone1.scb.net/sites/it-resilience/SitePages/ITR-Process-Templates.aspx](https://teamsites.zone1.scb.net/sites/it-resilience/SitePages/ITR-Process-Templates.aspx) |
| Application Restore Plan Template | [https://thebridge.zone1.scb.net/docs/DOC-689303](https://thebridge.zone1.scb.net/docs/DOC-689303) |
| Restore Plan Upload (SharePoint) | [https://standardcharteredbank.sharepoint.com/sites/cibtbcddcbinfrastructureservices/Shared%20Documents/Forms/AllItems.aspx?ga=1&](https://standardcharteredbank.sharepoint.com/sites/cibtbcddcbinfrastructureservices/Shared%20Documents/Forms/AllItems.aspx?ga=1&id=%2Fsites%2Fcibtbcddcbinfrastructureservices%2FShared%20Documents%2FIT%20Resilience%2FRestore%20Plans%20%2D%20Treatment%20Plan%20Remediation%2FFM%2FFinancial%20Markets&viewid=026c6c54%2D26e8%2D4099%2Dae2d%2D3a940fbcf746) [id=%2Fsites%2Fcibtbcddcbinfrastructureservices%2FShared%20Documents%2FIT%20Resilience%2FRestore%20Plans%20%](https://standardcharteredbank.sharepoint.com/sites/cibtbcddcbinfrastructureservices/Shared%20Documents/Forms/AllItems.aspx?ga=1&id=%2Fsites%2Fcibtbcddcbinfrastructureservices%2FShared%20Documents%2FIT%20Resilience%2FRestore%20Plans%20%2D%20Treatment%20Plan%20Remediation%2FFM%2FFinancial%20Markets&viewid=026c6c54%2D26e8%2D4099%2Dae2d%2D3a940fbcf746) [2D%20Treatment%20Plan%20Remediation%2FFM%2FFinancial%20Markets&viewid=026c6c54%2D26e8%2D4099%2Dae2d%2D3a940fbcf746](https://standardcharteredbank.sharepoint.com/sites/cibtbcddcbinfrastructureservices/Shared%20Documents/Forms/AllItems.aspx?ga=1&id=%2Fsites%2Fcibtbcddcbinfrastructureservices%2FShared%20Documents%2FIT%20Resilience%2FRestore%20Plans%20%2D%20Treatment%20Plan%20Remediation%2FFM%2FFinancial%20Markets&viewid=026c6c54%2D26e8%2D4099%2Dae2d%2D3a940fbcf746) |
| BOARD Portal (Data Backup Certification) | [https://board.gdc.standardchartered.com:8483/static/login](https://board.gdc.standardchartered.com:8483/static/login) |
| Test Environment Spec Guide | [https://confluence.global.standardchartered.com/display/SDF/Test+Environment+Specifications+-+User+Guide](https://confluence.global.standardchartered.com/display/SDF/Test+Environment+Specifications+-+User+Guide) |
| Test Environment Spec Template | [http://tpu.global.standardchartered.com/esdlc/core.default.prod_def.method.universal.base-scb/guidances/templates/resources/Test_Environment_Specification_Template%20(3).docx](http://tpu.global.standardchartered.com/esdlc/core.default.prod_def.method.universal.base-scb/guidances/templates/resources/Test_Environment_Specification_Template%20(3).docx) |
| ASRM Template | [http://tpu.global.standardchartered.com/esdlc/index.htm#core.default.prod_def.method.universal.base-scb/guidances/templates/sdf1_asrm_-_scb_FF5E19C2.html](http://tpu.global.standardchartered.com/esdlc/index.htm#core.default.prod_def.method.universal.base-scb/guidances/templates/sdf1_asrm_-_scb_FF5E19C2.html) |
| BRD Template | [http://tpu.global.standardchartered.com/esdlc/index.htm#core.default.prod_def.method.universal.base-scb/guidances/templates/sdf1_business_requirements_definition_brd_DB0D208.html](http://tpu.global.standardchartered.com/esdlc/index.htm#core.default.prod_def.method.universal.base-scb/guidances/templates/sdf1_business_requirements_definition_brd_DB0D208.html) |

### SNOW (ServiceNow Change Management)

| Purpose | Full URL |
| --- | --- |
| Change Category Reference | [https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) |