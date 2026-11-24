## **BPMS New Feature Onboarding Operational Readiness Questionnaire**

## 1. Business Context & Scope

*Define the business value, user base, and basic flow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **VAT Approval** | - VAT approval obtained. | **- VAT** **Approval: ** **[FSS Gating, SSI, CA Domestic and Gold Custody Change Request](https://confluence.global.standardchartered.com/display/DSP/FSS+Gating%2C+SSI%2C+CA+Domestic+and+Gold+Custody+Change+Request) - Approval Evidence** |
| **Functionality Description** | - Briefly describe the functionality to be built for the flow. | **- Functionality:** Enable business from FSS and VPA |
| **Current Business Handling** | - Existing Flow: How are this business currently handled? - New Interface: Respond as "New Interface". | - **Existing Flow: **NA - **New Interface:** 5 new tiles from FSS, 2 new tiles from VPA |
| **End-to-End Flow** | - Provide End-to-End Flow Diagram. - Include data flow, process/DB SP, sample message, E2E impact. | - **Diagram:** NA - **Details:** [FSS Gating, SSI, CA Domestic and Gold Custody Change Request](https://confluence.global.standardchartered.com/display/DSP/FSS+Gating%2C+SSI%2C+CA+Domestic+and+Gold+Custody+Change+Request) - **Details: **[VPA Fix-link and Monitor Change Request](https://confluence.global.standardchartered.com/display/DSP/VPA+Fix-link+and+Monitor+Change+Request) |
| **Interfaces & Data Feeds** | - What are the interfaces and data face to be introduced? - Interface Type (Real-time, Batch, etc.)? - If Batch: How many data feeds? Provide details. | - **Interfaces:** `[Upstream SFTP, Downstream API]`. - **Type:** NA `[Batch, Real-time ]`. - **Batch Count:** NA `[3 Daily Feeds]` |
| **Scope (Country/Product)** | - Rollout Country/Entity? - Product/Asset Class involved? | - **Country/Entity:** Global`[UK, US, HK Entities]`. - **Product/Asset:**`[Equities, FX, Fixed Income]`. |
| **Clients & Users** | - Client Type (Internal, External, Regulatory)? - Number of users introduced? - User location? | - **Client Type:** `[Internal Operations & External Counterparties].` - **User Count:** 41 for FSS, 50 for VPA.`[Approx. 50 Named Users]`. - **User ****Location:** Global`[London, New York, Singapore]` |
| **Volume & Business Hours** | - Daily Volume & Peak Volume? - Business Hours & Peak Hour? | **- Volume:** Max concurrent user count 25`[Avg 10k/day, Peak 2k/hour]`. - **Business** **Hours:** NA`[08:00 - 18:00 GMT]`. - **Peak Hour:** NA`[09:00 - 11:00 GMT]` |
| **Support Hours** | - Expected support hours defined (e.g., 8*5, 24*5). - BAU model defined for **Static Data, Interface Control, Monitoring, Alerting, Tracking, Reporting, License/key renew, Restart/Reboot/Patching.** | - **Hours:** NA`[Defined: 24x5]`. - **BAU Model:** NA`[Documented for all areas]` |
| **Release Plan** | - Release frequency (Single, Half-yearly, Quarterly, Monthly, Weekly) and planned upgrade schedule. | - **Release ****Frequency:** Monthly`[Monthly]`. - **Next Upgrade:** 2026-08-15`[2026-11-01]` |
| **Tech Stack & Infrastructure** | - New Technology Stack involved? - New Infrastructure (Server, Hardware, Network)? - Provide Architecture Diagram. | - **Stack:** NA`[Java 17, Spring Boot, PostgreSQL]`. - **Infra:** NA`[AWS EC2, RDS, Load Balancer]`. - **Diagram:** NA`[High-Level Architecture Attached]` |
| **Vendor Management** | - If vendor product is used: Share contract details (contract, ER, renewal date, vendor contact) and issue raising procedure. | - **Vendor:** NA`[No 3rd Party Vendor Used]`. - **Contract: **NA `[N/A]`. |
| **Certificates** | - If any new certificates/licenses. | - **Certificates:** `[Certificates/licenses details Certificate expiry Period]` |

## 2. Operational Resilience & Exception Handling

*Core operational requirements. **Test evidence must be provided for each checkpoint.**.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **E2E Flow Control** | - Ensure successful message delivery. - Raise exception to responsible team on time. - ACK/NACK mechanism or E2E reconciliation in place. - Validation on Completeness & Accuracy. | - **Delivery:** `[Guaranteed via Persistent Queue]`. - **Exception:** `[Alerts sent within 5 mins via ServiceNow]`. - **ACK/NACK:** `[Implemented at Protocol Level]`. - **Validation:** `[Checksum & Record Count Validation]` |
| **Auto Resume (Connectivity)** | - Auto resume connectivity (continuously re-try mechanism) with upstream/downstream/middleware. - **No manual intervention required.** | - **Auto Resume:** `[Exponential Backoff Retry Implemented]`. - **Manual Intervention:** `[None Required]` |
| **Infrastructure Issue Handling** | - Able to stop process in case of infra issue (DB, Unix, Network, TDE). - Resume process automatically without data loss/partial processing once resolved. | - **Stop Process:** `[Graceful Shutdown on Signal]`. - **Auto Resume:** `[Pending Messages Re-processed on Restart]` |
| **Single Message Failure** | - Able to handle single message failure automatically without stopping/suspending application process. | - **Handling:** `[Failed Messages routed to Dead Letter Queue (DLQ)]`. - **Process Status:** `[Main Process Continues Uninterrupted]` |
| **DB Transaction Management** | - Done properly to ensure system can be gracefully shutdown without any message stuck, lost, or partially processed. | - **Transaction:** `[All Writes are Atomic/Transactional]`. - **Shutdown:** `[No In-Flight Data Loss]` |
| **Exception Categorization** | - Properly categorize exception type (Technical vs. Data). - Auto recover technical issues (e.g., infra outage). - Route data issues to responsible team. | - **Exception** **Categorization:** `[Error Codes Defined (5xx vs 4xx)]`. - **Auto Recover:** `[Technical Errors Retry Automatically]`. - **Data Issues:** `[Alerts Sent to Ops Team for Review]` |
| **DR Configuration** | - Both Production and DR sites configured without single point of failure. - No configuration change required for DR switchover. | - **DR Sites:** `[Active-Passive Configured]`. - **Switchover:** `[DNS Based, No Code Change Needed]` |
| **File Handling** | - In case of file download failure, able to re-download automatically without manual intervention. | - **Re-download:** `[SFTP Connector Auto-Retry Enabled]`. - **Manual Intervention:** `[None Required]` |
| **Database Health** | - Ensure no bad execution plan introduced for new SQL/SP. - Ensure no invalid DB objects introduced by DB change. | - **Execution Plan:** `[Reviewed & Optimized]`. - **DB Objects:** `[All Objects Validated Post-Deploy]` |
| **Automatic Housekeeping** | - Automatic housekeeping in-place (Files, DB, Temp, Logs, Inbound/Outbound). - If missing, CRISP to cover with remediation plan. - **ASRM Details:** Job name, Frequency, Target details. | - **Housekeeping:** `[Job HK_CLEANUP Implemented]`. - **CRISP:** `[Not Required]`. - **ASRM:** `[Job: HK_CLEANUP, Freq: Daily 02:00, Target: 30 Days Retention]`. |
| **Manual Tasks** | - **No manual tasks** will be introduced by this release. | - **Manual Tasks:** `[Zero Manual Tasks for BAU]` |
| **Logging** | - Logging in place with proper level (INFO, WARN, ERROR). - Details stated in ASRM. - Standardized service log pattern for monitoring tool capture. | - **Levels:** `[INFO, WARN, ERROR Configured]`. - **ASRM:** `[Details Included in ASRM]`. - **Pattern:** `[JSON Format for Splunk Ingestion]` |
| **Holiday & Greenzone** | - Proper agreement on Holiday cases (auto handling). - Job schedules avoid Greenzone window. - Green Zone agreed in OLA/SLA for weekend activities. | - **Holiday:** `[Jobs Paused on Bank Holidays]`. - **Greenzone:** `[No Jobs Scheduled 22:00-02:00]`. - **OLA/SLA:** `[Agreed in Document OLA-005]` |

---

## 3. Automation & Deployment

*Automation is mandatory to reduce operational risk.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Service Control** | - One-click stop/start of all services & single service. | - **Control:** `[Scripts Available in ADO for Full/Single Service]` |
| **Deployment** | - **One-click deployment using ADO pipeline.** - Any other method requires dispensation approval. | - **Deployment:** `[CI/CD Pipeline Configured in ADO]`. - **Other Method:** `[None Used]` |
| **Disaster Recovery** | - **One-click DR** switchover. | - **Switchover:** `[Button Available in Control Dashboard]` |
| **Server Maintenance** | - Server patching via ADO pipeline (auto maintenance window). - Auto Server reboot (via CR if touch token not used). | - **Patching:** `[Automated via Ansible/ADO]`. - **Reboot:** `[Automated via Change Request]` |
| **Fully Automated Operations** | - Automated restart, deployment, DR, and housekeeping. | - **Operations:** `[All Key Operations Automated]` |

---

## 4. Monitoring & Alerting

*Ensure production visibility and proactive alerting.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Application Status** | - Health check/status monitor from **ITRS** for all components/services/API/GUI. | - **ITRS Probe:** `[Deployed for all components]`. - **Coverage:** `[Services, API, GUI monitored]` |
| **Interface Connectivity** | - All real-time interface connectivity health check. - Batch file receiving/sending monitoring. - Batch processing monitoring. | - **Real-time:** `[Checks active via Heartbeat]`. - **Batch File:** `[Monitors active for In/Out]`. - **Processing:** `[Latency monitored per job]` |
| **Infrastructure Monitoring** | - Infra connectivity (DB, Solace, MQ, OUD, MFA, Kafka, Redis, etc.). - Network, Disk space, Filesystem. - DB space, long running query, blocking session, active session count. | - **Connectivity:** `[All components monitored (DB, MQ, Kafka)]`. - **Infra:** `[Disk/Network alerts configured]`. - **DB Health:** `[Space, Queries, Sessions active]` |
| **Capacity Monitoring** | - CPU/Memory utilization < 70%. (for active-passive, if it's active-active cluster then 2 nodes added together <70%). - Disk/DB space utilization < 70% ((for active-passive, if it's active-active cluster then 2 nodes added together <70%).) - Trade volume monitoring (Hourly/Daily/Weekly). | - **CPU/Mem:** `[Threshold set at 70%]`. - **Disk/DB:** `[Threshold set at 70%]`. - **Volume:** `[Trade Volume monitor configured]` |
| **Transaction Monitoring** | - All messages processed as expected. - Detect abnormal trade processing or stuck trades in intermediate status. - MQ/Kafka pending message queue monitoring. | - **Messages:** `[Transaction logs monitored]`. - **Stuck Trades:** `[Alerts configured for intermediate status]`. - **Queue:** `[MQ/Kafka Queue depth monitored]` |
| **Performance & SLA/OLA** | - Processing throughput and latency monitoring. - Key deliveries meet SLA requirements. - Meet expected cutoff following OLA. | - **Performance:** `[Throughput/Latency monitor available]`. - **SLA:** `[SLA metrics tracked]`. - **OLA:** `[Cutoff alerts enabled]` |
| **Certificates** | - Expiry day monitor for all in-use certificates/licenses. | - **Monitor:** `[Certificate expiry alert set (30 days prior)]` |

---

## 5. Support Model & Access Management

*Define who supports the app and how access is controlled.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Vaulting & Accounts** | - All prod accounts vaulted (Hashicorp/One-Vault). - PSS Read-only accounts ready (DB, Server, Software) before Go-Live. - Security Matrix ready. | - **Vaulting:** `[Secrets vaulted in Hashicorp]`. - **Accounts:** `[Read-only accounts created]`. - **Matrix:** `[Security Matrix ready]` |
| **File Access** | - All files (config, inbound, outbound, logs) viewable by PSS read-only accounts. **No 777 access** to prod files. | - **Permissions:** `[Confirmed: Permissions set to 640]`. - **Access:** `[PSS has read access]`. - **Security:** `[No 777 access found]` |
| **ITRS Privilege** | - ITRS interactive privilege ID to STOP & START the ITRS netprobe process. | - **ID Provided:** `[ITRS_ID_123]` |
| **User Access Management** | - Centralized management by OneCert. - Access request automated via SRM (UAM/IAM, ULA, URA). - **MFA onboarded** for user authentication. | - **Management:** `[OneCert Integrated]`. - **Automation:** `[Access request automated]`. - **MFA:** `[Enabled for all users]` |

---

## 6. Documentation & Compliance

*Ensure knowledge transfer and audit compliance. Provide links or attachments.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **OLA (Operational Level Agreement)** | - PSS Manager sign-off. (If OLA is not required, PSS Manager to provide email confirmation) - Developed per OLA template - Uploaded to OLA Central Repository | - **Sign-off:** `[Signed off by PSS Manager]`. - **Template:** `[OLA Template Used]`. - **Repository:** `[Uploaded to OLA Central Repository]` |
| **SLA (Service Level Agreement)** | - BO (Business Owner) sign-off. (If SLA is not required, BO need provide email sign off with justification) - Developed per SLA template. - Uploaded to SLA Central Repository. | - **Sign-off:** `[Signed off by BO]`. - **Template:** `[SLA Template Used]`. - **Repository:** `[Uploaded to SLA Central Repository]` |
| **Capacity Plan (**If capacity plan is not required, TSM to email Capacity Team with justification of why it is not required**)** | - Created in M7 System. - Aligned with FM Capacity Analytics tool. - If not required, TSM to email Capacity Team with justification. | - **System:** `[Created in M7]`. - **Alignment:** `[Aligned with FM Tool]` |
| **Service Recovery Plans** | - **Service Recovery Plan:** Developed per template (ITR Process Templates), uploaded to M7. - **Application Restore Plan:** Developed per template, uploaded to SharePoint/M7. | - **SRP:** `[Uploaded to M7]`. - **ARP:** `[Uploaded to M7]` |
| **Data Backups** | - Data backups certified in BOARD Portal. | - **Certification:** `[Certified]`. - **Ref Number:** `[Backup-Ref-123]` |
| **Test Environment Specification** | - Test Environment Specification completed (Overview, Architecture, Config, Prod vs Test, RAID). - Test Environment Specification template and guide, kindly refer to Appendix | - **Spec:** `[Spec Completed, link]`. - **Template:** `[Template Followed]` |
| **ASRM ** | - Data workflow diagram included. - General Troubleshooting guideline (SQL, Log keywords). - Housekeeping details included. - Kindly refer to ASRM template in Appendix | - **Diagram:** `[Included]`. - **Guidelines:** `[Added]`. - **Housekeeping: **`[Detail provided]`**.** |
| **Business & Ops Docs** | - BRD (Business Requirements Definition) developed via BRD template. - Operational Runbook / SOP / DOI available. - DASH Onboarding for data extraction. | - **BRD:** `[Approved]`. - **Runbook:** `[Runbook/SOP/DOI Available]`. - **DASH:** `[Onboarded]`. |

---

## 7. Change Management (ServiceNow & AIG)

*Ensure the release process follows change management standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [FSS Gating, SSI, CA Domestic and Gold Custody Change Request](https://confluence.global.standardchartered.com/display/DSP/FSS+Gating%2C+SSI%2C+CA+Domestic+and+Gold+Custody+Change+Request) [VPA Fix-link and Monitor Change Request](https://confluence.global.standardchartered.com/display/DSP/VPA+Fix-link+and+Monitor+Change+Request) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | Add 5 FSS new tiles Add 2 VPA new tiles |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | TBD |
| - Regression Test Evidence (Link or Attachment, Comment if NA) | TBD |
| - Performance Test Evidence (Link or Attachment, Comment if NA) | NA |
| - UAT Sign-off (Link or Attachment, Comment if NA) | FSS UAT Signoff [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15014893#19498325](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15014893#19498325) VPA UAT Signoff [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15390798#19803005](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15390798#19803005) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | NA |
| **Implement Plan** | - Attestation if any manual steps | NA |
| **UVT plan** | - List details of UVT plan for each story | [Release On 2026-08-15 CR:CHG1037739 Markets Operations One](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-08-15+CR%3ACHG1037739+Markets+Operations+One) - UVT |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | NA |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | NA |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | NA |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | Done |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | **OLA: TBD** |
| - PSS Core Function confluence page - PSS Interface confluence page | NA |
| **Monitor** | - Attestation if any monitoring need add or update | FSS: container.keyword : \"fss_funds_gating\" or container.keyword : \"fss_gold_custody\" or container.keyword : \"fss_ca_domestic_disbursement\" or container.keyword : \"fss_ssi\" or container.keyword : \"da_collateral_management_tile\" VPA: container.keyword : \"fix-link\" or container.keyword : \"monitor\" |

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