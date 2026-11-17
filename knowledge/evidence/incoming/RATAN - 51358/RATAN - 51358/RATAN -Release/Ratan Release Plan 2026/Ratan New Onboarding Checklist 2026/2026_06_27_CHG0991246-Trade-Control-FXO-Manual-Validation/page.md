# **BPMS New Feature Onboarding Operational Readiness Questionnaire**

**Project Name:** RATAN
**Application Name:** RATAN
**Change Request ID:** CHG0991246
**Date:** 27/06/2026
**DEV Owner/Lead:** Jay
**PSS :** Jane

## 1. Business Context & Scope

*Define the business value, user base, and basic flow.*

| ID | Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- | --- |
| **1.1** | **Current Business Handling** | - Existing Flow: How are this business currently handled? - New Interface: Respond as "New Interface". | - **Existing Flow:** **Enhancement: ** 11372548 - Netting Trade Validation 12913457 - onboard new fields to fiter/view/Rule Blotter for Credit 13091199 - Onboarding new fields for G10 in RATAN 13129615 - User able to copy the counterparty FM ID from the search panel **Bug Fix:** 13383014 - [Bug] Missing dropdown description for payment holiday using "View Contract" 13515275 - TC- multileg - Shouldn't have 'Contract Validation' button when selected multiple trades 13528578 - TC - payment schedule - Shouldn't display cashflow that event type is 'withdrawal' in payment schedule 13542952 - [Bug] Incorrect validation static when using MO comment 13559974 - TC - Fields should be remove for ForeignExchange:SimpleExotic:Barrier Product_Sub_Type: Double Barrier 13561784 - TC- Missing value in Contract comparison 13688887 - [Bug Trade - Control] Coupon captured in Other Cashflow 13847487 - [Trade Control] FXO - Missing fixing source in Ratan 14364433 - [Trade Control] FXO - Incorrect notional in View Contract - **New Interface:** 7461950 - UI Enhancement for multi leg FXO and validation for whole Contract 10088881 - display trades netting results for FXO 11510326 - View Contract to be added under Trade Blotter 11886843 - Implement FXO Contract Validation Design and Enhanced Add Comment Handling 11965200 - Enhance Trade Ticket for Barrier, Double Barrier, Digital, Barrier Digital, and Double Barrier Digital Products 12189506 - Trade Blotter: Onboard Touch product with template in Trade Details 12205563 - Display historical netted trade in "History" 12351516 - [Trade Control] Enhancement for Story 9885389 - History in Trade Blotter 12442354 - New entities onboarding FXO (including G10/india) 12750899 - Enhance Trade Ticket for Vanilla, NDO, Barrier, Double Barrier, Digital, Barrier Digital, and Double Barrier Digital Products (2) 13129615 - User able to copy the counterparty FM ID from the search panel 13442127 - Query and integrate "FMCODE" into "Additional Payment" table & "Other Cashflows" 13514464 - Comments should appear in MO Exception blotter front display 13661211 - [FXO] Enhance Trade Ticket for FX Barrier and Digital 13717640 - Enhance FX Barrier field display logic - Barrier Style 13799885 - "View Contract" UI enhancement 13808986 - Adjust logical field of compounding calc for IR CCS/Swap 14004361- [Trade Control] Discontinue of ECONFAFFIRMED workflow in FMRP - Remove "ECON AFFIRMED" from Validation Status in Ratan **Other ** [Story 12160039](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12160039): Integrate Falcon API to get FX rate and bond price for C&A processing BTS trades. |
| **1.2** | **Functionality Description** | Briefly describe the functionality to be built for the flow. | - ** Functionality:** support FXO products / netted trades in trade ticket and contract validation; Enhance history tab with more columns including netting history |
| **1.3** | **Scope (Country/Product)** | - Rollout Country/Entity? - Product/Asset Class involved? | - **Country/Entity:** UK - **Product/Asset:** FXO |
| **1.4** | **Clients & Users** | - Client Type (Internal, External, Regulatory)? - Number of users introduced? - User location? | - **Client Type:** `Internal Operations` - **User Count:** 2`0 Named Users]`. - **User ****Location:** `London` |
| **1.5** | **Volume & Business Hours** | - Daily Volume & Peak Volume? - Business Hours & Peak Hour? | **- Volume:** `Avg 100k/day, Peak 10k/hour` - **Business** **Hours:** `08:00 - 18:00 GMT` - **Peak Hour:** 2`1:00 GMT` |
| **1.6** | **Release Plan** | Release frequency (Single, Half-yearly, Quarterly, Monthly, Weekly) and planned upgrade schedule. | - **Release ****Frequency:** `Monthly`. - **Next Upgrade:** `2026-07-04` |

---

## 2. Architecture & System Onboarding

*Assess technical implementation, interface standards, and system registration.*

| ID | Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- | --- |
| **2.1** | **End-to-End Flow** | - Provide End-to-End Flow Diagram. - Include data flow, process/DB SP, sample message, E2E impact. | - **Diagram:** Same like Trade control work flow - **Details:** Includes scbml |
| **2.2** | **Interfaces & Data Feeds** | - What are the interfaces and data face to be introduced? - Interface Type (Real-time, Batch, etc.)? - If Batch: How many data feeds? Provide details. | - **Interfaces:** Upstream - TDS3. Downstream - RAZOR - **Type:** ` Real-time` - **Batch Count:** `NA` |
| **2.3** | **Tech Stack & Infrastructure** | - Technology Stack involved? - Infrastructure (Server, Hardware, Network)? - Provide Architecture Diagram. | - **Stack:** Java , React **Infra:** uklvapapp590,uklvapapp591,uklvapapp676 uklvasapp590,uklvasapp591,uklvapapp676 - **Diagram:** NA |
| **2.4** | **System Registration** | - [ ] App onboarded in **CMDB**. - [ ] App ready in **ServiceNow**. - [ ] App ready in **ADO** (Azure DevOps). | - **CMDB:** 51358 - **ServiceNow:** 51358 - **ADO:** `FMQPR/51358` |
| **2.5** | **Naming Conventions** | - [ ] Application code/package folder naming follows standard. - [ ] Control-M Job/Smartfolder naming follows standard. - [ ] Inbound/Outbound folder/path naming follows standard. | - **Code Naming:** 51358-ratanone-ansible - **Control-M:** NO - **Folders:** No |
| **2.6** | **Vendor Management** | If vendor product is used: Share contract details (contract, ER, renewal date, vendor contact) and issue raising procedure. | - **Vendor:** No - **Contract:** No |

---

## 3. Operational Resilience & Exception Handling

*Core operational requirements. **Test evidence must be provided for each checkpoint.**.*

| ID | Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- | --- |
| **3.1** | **E2E Flow Control** | - [ ] Ensure successful message delivery. - [ ] Raise exception to responsible team on time. - [ ] ACK/NACK mechanism or E2E reconciliation in place. - [ ] Validation on Completeness & Accuracy. | - **Delivery:** Trade control work flow - **Exception:** Manual handle by user - **ACK/NACK:** Trade control work flow - **Validation:** Manual handle by user |
| **3.2** | **Auto Resume (Connectivity)** | - [ ] Auto resume connectivity (continuously re-try mechanism) with upstream/downstream/middleware. - [ ] **No manual intervention required.** | - **Auto Resume:** `follow Trade control work flow` - **Manual Intervention:** `No` |
| **3.3** | **Infrastructure Issue Handling** | - [ ] Able to stop process in case of infra issue (DB, Unix, Network, TDE). - [ ] Resume process automatically without data loss/partial processing once resolved. | - **Stop Process:** `same like before` - **Auto Resume:** `same like before` |
| **3.4** | **Single Message Failure** | Able to handle single message failure automatically without stopping/suspending application process. | - **Handling:** `Manual handle by user` - **Process Status:** `No change` |
| **3.5** | **DB Transaction Management** | Done properly to ensure system can be gracefully shutdown without any message stuck, lost, or partially processed. | - **Transaction:** `same like before, no new trades add` - **Shutdown:** `same like before` |
| **3.6** | **Exception Categorization** | - [ ] Properly categorize exception type (Technical vs. Data). - [ ] Auto recover technical issues (e.g., infra outage). - [ ] Route data issues to responsible team. | - **Exception** **Categorization:** `Manual handle by user` - **Auto Recover:** `same like before` - **Data Issues:** `same like before` |
| **3.7** | **DR Configuration** | - [ ] Both Production and DR sites configured without single point of failure. - [ ] No configuration change required for DR switchover. | - **DR Sites:** `same like before` - **Switchover:** `same like before` |
| **3.8** | **File Handling** | In case of file download failure, able to re-download automatically without manual intervention. | - **Re-download:** `No need` - **Manual Intervention:** `No need ` |
| **3.9** | **Database Health** | - [ ] Ensure no bad execution plan introduced for new SQL/SP. - [ ] Ensure no invalid DB objects introduced by DB change. | - **Execution Plan:** `same like before` - **DB Objects:** `same like before` |
| **3.10** | **Automatic Housekeeping** | - [ ] Automatic housekeeping in-place (Files, DB, Temp, Logs, Inbound/Outbound). - [ ] If missing, CRISP to cover with remediation plan. - [ ] **ASRM Details:** Job name, Frequency, Target details. | - **Housekeeping:** `same like before` - **CRISP:** `same like before` - **ASRM:** `same like before` |
| **3.11** | **Manual Tasks** | - [ ] **No manual tasks** will be introduced by this release. | - **Manual Tasks:** `No manual task` |
| **3.12** | **Logging** | - [ ] Logging in place with proper level (INFO, WARN, ERROR). - [ ] Details stated in ASRM. - [ ] Standardized service log pattern for monitoring tool capture. | - **Levels:** `same like before` - **ASRM:** `same like before` - **Pattern:** `same like before` |
| **3.13** | **Holiday & Greenzone** | - [ ] Proper agreement on Holiday cases (auto handling). - [ ] Job schedules avoid Greenzone window. - [ ] Green Zone agreed in OLA/SLA for weekend activities. | - **Holiday: ** `same like before` - **Greenzone:** `same like before` - **OLA/SLA: ** `same like before` |

---

## 4. Automation & Deployment

*Automation is mandatory to reduce operational risk.*

| ID | Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- | --- |
| **4.1** | **Service Control** | - [ ] One-click stop/start of all services & single service. | - **Control:** `Scripts Available in ADO for Full/Single Service` |
| **4.2** | **Deployment** | - [ ] **One-click deployment using ADO pipeline.** - [ ] Any other method requires dispensation approval. | - **Deployment:** `CI/CD Pipeline Configured in ADO` - **Other Method:** `None Used` |
| **4.3** | **Disaster Recovery** | - [ ] **One-click DR** switchover. | - **Switchover:** `Button Available in Control Dashboard` |
| **4.4** | **Server Maintenance** | - [ ] Server patching via ADO pipeline (auto maintenance window). - [ ] Auto Server reboot (via CR if touch token not used). | - **Patching:** `Automated via Ansible/ADO` - **Reboot:** `Automated via Change Request` |
| **4.5** | **Fully Automated Operations** | - [ ] Automated restart, deployment, DR, and housekeeping. | - **Operations:** `All Key Operations Automated` |

---

## 5. Monitoring & Alerting

*Ensure production visibility and proactive alerting.*

| ID | Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- | --- |
| **5.1** | **Application Status** | Health check/status monitor from **ITRS** for all components/services/API/GUI. | - **ITRS Probe:** `Deployed for all components` - **Coverage:** `Services, API, GUI monitored` |
| **5.2** | **Interface Connectivity** | - [ ] All real-time interface connectivity health check. - [ ] Batch file receiving/sending monitoring. - [ ] Batch processing monitoring. | - **Real-time:** `Checks active via Heartbeat` - **Batch File:** `Monitors active for In/Out` - **Processing:** `Latency monitored per job` |
| **5.3** | **Infrastructure Monitoring** | - [ ] Infra connectivity (DB, Solace, MQ, OUD, MFA, Kafka, Redis, etc.). - [ ] Network, Disk space, Filesystem. - [ ] DB space, long running query, blocking session, active session count. | - **Connectivity:** `All components monitored (DB, MQ, Kafka)` - **Infra:** `Disk/Network alerts configured` - **DB Health:** `Space, Queries, Sessions active` |
| **5.4** | **Capacity Monitoring** | - [ ] CPU/Memory utilization < 70%. (for active-passive, if it's active-active cluster then 2 nodes added together <70%). - [ ] Disk/DB space utilization < 70% ((for active-passive, if it's active-active cluster then 2 nodes added together <70%).) - [ ] Trade volume monitoring (Hourly/Daily/Weekly). | - **CPU/Mem:** `Threshold set at 70%` - **Disk/DB:** `Threshold set at 70%` - **Volume:** `Trade Volume monitor configured` |
| **5.5** | **Transaction Monitoring** | - [ ] All messages processed as expected. - [ ] Detect abnormal trade processing or stuck trades in intermediate status. - [ ] MQ/Kafka pending message queue monitoring. | - **Messages:** `Transaction logs monitored` - **Stuck Trades:** `Alerts configured for intermediate status` - **Queue:** `MQ/Kafka Queue depth monitored` |
| **5.6** | **Performance & SLA/OLA** | - [ ] Processing throughput and latency monitoring. - [ ] Key deliveries meet SLA requirements. - [ ] Meet expected cutoff following OLA. | - **Performance:** `Throughput/Latency monitor available` - **SLA:** `SLA metrics tracked` - **OLA:** `Cutoff alerts enabled` |
| **5.7** | **Certificates** | Expiry day monitor for all in-use certificates/licenses. | - **Monitor:** `Certificate expiry alert set (30 days prior)` |

---

## 6. Support Model & Access Management

*Define who supports the app and how access is controlled.*

| ID | Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- | --- |
| **6.1** | **PSS Early Engagement** | - [ ] Engagement Plan: Engage SME and PSS Manager ASAP. - [ ] Fill up onboarding checklist to assess PSS support effort. - [ ] Identify PSS SPOC. - [ ] Update interface confluence accordingly | - **Engagement:** `PSS Engaged` - **Checklist:** `Completed` - **SPOC:** `Grace` - **Interface page updated:** [Release On 2026-06-13 CR: CHG0991246 Trade Control - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-06-13+CR%3A+CHG0991246+Trade+Control) |
| - [ ] Expected support hours defined (e.g., 8*5, 24*5). - [ ] BAU model defined for **Static Data, Interface Control, Monitoring, Alerting, Tracking, Reporting, License/key renew, Restart/Reboot/Patching.** | - **Hours:** `Defined: 24x5` - **BAU Model:** `Documented for all areas` | | |
| **6.3** | **Vaulting & Accounts** | - [ ] All prod accounts vaulted (Hashicorp/One-Vault). - [ ] PSS Read-only accounts ready (DB, Server, Software) before Go-Live. - [ ] Security Matrix ready. | - **Vaulting:** `Secrets vaulted in Hashicorp` - **Accounts:** `Read-only accounts created` - **Matrix:** `Security Matrix ready` |
| **6.4** | **File Access** | All files (config, inbound, outbound, logs) viewable by PSS read-only accounts. **No 777 access** to prod files. | - **Permissions:** `Confirmed: Permissions set to 640` - **Access:** `PSS has read access` - **Security:** `No 777 access found` |
| **6.5** | **ITRS Privilege** | ITRS interactive privilege ID to STOP & START the ITRS netprobe process. | - **ID Provided:** `ITRS_ID_123` |
| **6.6** | **User Access Management** | - [ ] Centralized management by OneCert. - [ ] Access request automated via SRM (UAM/IAM, ULA, URA). - [ ] **MFA onboarded** for user authentication. | - **Management:** `OneCert Integrated` - **Automation:** `Access request automated` - **MFA:** `Enabled for all users` |
| **6.7** | **VAT Approval** | - [ ] VAT approval obtained. | **- VAT** **Approval:** `VAT Approved` |

---

## 7. Documentation & Compliance

*Ensure knowledge transfer and audit compliance. Provide links or attachments.*

| ID | Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- | --- |
| **7.1** | **OLA (Operational Level Agreement)** | - [ ] PSS Manager sign-off. (If OLA is not required, PSS Manager to provide email confirmation) - [ ] Developed per OLA template - [ ] Uploaded to OLA Central Repository | - **Sign-off:** `Signed off by PSS Manager` - **Template:** `OLA Template Used` - **Repository:** `Uploaded to OLA Central Repository` |
| **7.2** | **SLA (Service Level Agreement)** | - [ ] BO (Business Owner) sign-off. (If SLA is not required, BO need provide email sign off with justification) - [ ] Developed per SLA template. - [ ] Uploaded to SLA Central Repository. | - **Sign-off:** `Signed off by BO` - **Template:** `SLA Template Used` - **Repository:** `Uploaded to SLA Central Repository` |
| **7.3** | **Capacity Plan (**If capacity plan is not required, TSM to email Capacity Team with justification of why it is not required**)** | - [ ] Created in M7 System. - [ ] Aligned with FM Capacity Analytics tool. - [ ] If not required, TSM to email Capacity Team with justification. | - **System:** `Created in M7` - **Alignment:** `Aligned with FM Tool` |
| **7.4** | **Service Recovery Plans** | - [ ] **Service Recovery Plan:** Developed per template (ITR Process Templates), uploaded to M7. - [ ] **Application Restore Plan:** Developed per template, uploaded to SharePoint/M7. | - **SRP:** `Uploaded to M7` - **ARP:** `Uploaded to M7` |
| **7.5** | **Data Backups** | - [ ] Data backups certified in BOARD Portal. | - **Certification:** `Certified` - **Ref Number:** `Backup-Ref-123` |
| **7.6** | **Test Environment Specification** | - [ ] Test Environment Specification completed (Overview, Architecture, Config, Prod vs Test, RAID). - [ ] Test Environment Specification template and guide, kindly refer to Appendix | - **Spec:** `Spec Completed, link` - **Template:** `Template Followed` |
| **7.7** | **ASRM ** | - [ ] Data workflow diagram included. - [ ] General Troubleshooting guideline (SQL, Log keywords). - [ ] Housekeeping details included. - [ ] Kindly refer to ASRM template in Appendix | - **Diagram:** `Included` - **Guidelines:** `Added` - **Housekeeping: **`Detail provided` |
| **7.8** | **Business & Ops Docs** | - [ ] BRD (Business Requirements Definition) developed via BRD template. - [ ] Operational Runbook / SOP / DOI available. - [ ] DASH Onboarding for data extraction. | - **BRD:** `Approved` - **Runbook:** `Runbook/SOP/DOI Available` - **DASH:**`Onboarded` |

---

## 8. Change Management (ServiceNow & AIG)

*Ensure the release process follows change management standards.*

| ID | Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- | --- |
| **8.1** | **ServiceNow Change Request** | - [ ] Category/Subcategory based on change nature. - [ ] Short Description meaningful and accurate. - [ ] Description includes related ADO work item/story. - [ ] Justification includes details of new flow/feature. - [ ] Affected CIs list confirmed. | - **CR Number:** CHG0991246 - **Description:** RATAN Trade Control Monthly Release - Jun - **ADO Links:** [Release-2026Jun - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/ec03d0e7-dc86-409c-99b3-7d8ab5d43ddd/) - **CIs:** `RATAN` `[2026_06_13_CHG0991246-Trade-Control-Monthly-release - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/2026_06_13_CHG0991246-Trade-Control-Monthly-release)` |
| **8.2** | **Change Attachments** | - [ ] Change test sign-off (Functional, Regression, Performance, DR). - [ ] BPMS_Pre-CAB_Checklist with SME sign-off. - [ ] UAT sign-off (for functional changes). - [ ] AIG and AIG test sign-off. | - **Sign-offs:** `[All Sign-offs Attached]`. - **Checklist:** `[Signed off]`. - **UAT/AIG:** `[Signed off]`. |
| **8.3** | **Implementation Plan (AIG)** | - [ ] Includes Deployment details, UVT Verification, Rollback Plan. - [ ] **ADO pipeline is the only option** for deployment. (Anything else need dispensation approval from Gevin/Jane/Edward.) | - **Plan:** In CR - **Pipeline:** `In ADO` |
| **8.4** | **Scheduling & Booking** | - [ ] Change window covers UVT and Rollback. - [ ] Downtime outside greenzone has BO approval. - [ ] PSS resource booked (2 hours max per CR). | - **Window:** 20/06/2026 - **Approval:** - **Resources:** |
| **8.5** | **SOW/SOD Health Check** | - [ ] SOW/SOD health check instruction updated in Confluence. | - **Update:** |

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*

# Appendix:

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