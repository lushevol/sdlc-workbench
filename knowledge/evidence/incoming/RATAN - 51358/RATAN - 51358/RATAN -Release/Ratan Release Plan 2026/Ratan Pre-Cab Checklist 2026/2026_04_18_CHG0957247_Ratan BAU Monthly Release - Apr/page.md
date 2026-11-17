# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** Ratan
**Application Name:** Ratan
**Change Request ID:** CHG0957247
**Date:** 18/04/2026
**DEV Owner/Lead:** Nick
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | RATAN BAU Monthly Release - Apr |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Release 12931708 RATAN BAU Monthly Release - Apr](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12931708) [Subtask 12723491 [DevOps] Kafka & cluster restart scripts enhancement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12723491) [Generic Task 13005509 RATANONE Prod dumps fully backup](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13005509) [Story 12428137 LMS remove the entity filter](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12428137) [Story 12362685 [ISO] Hybrid Address Enhancement in Calling SSI+](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12362685) [Story 13128309 [RATANONE BAU]Enhance Query Validation for Quick Search & Custom Filter](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13128309) [Story 13150190: [Swift] Enhance the swift message generation function When withdrawal cashflow - Boards](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13150190) [Story 11544026 New API for CIS](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11544026/?view=edit) [Story 11999588 Data Entitlement on BCS Blotter](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11999588/?view=edit) [Story 12776468 [Dashboard] Pending in Group blotter post manual delivery](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12776468/?view=edit) [Bug 13150711 [User Friendly] [LOANIQ] Should move status to SETTLED after receive 'ACK' msg from downstream](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13150711/?view=edit) [Bug 13151033 [User Friendly] Trade Status displayed as VALD instead of COMP](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13151033/?view=edit) [Bug 13184479 [User Friendly] Bic netting error on historical cashflow after bic netting update + reinstate](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13184479/?view=edit) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | 1. Update Kafka script to graceful shutdown and avoid force kill, make Kafka startup successfully before backend services start (restart cluster while one server lost ?) 2. ~~RFI Nostro stamping based on Portfolio (Reject)~~ 3. PG dump scripts update to backup fully data for some big table (dump size in story) 4. LMS remove filter for entities which need to generate LMS message (OLA ?) 5. Call SSI+ with hybrid address 6. Enhance Query Validation in UI for Quick Search & Custom Filter (DOI) 7. Swift cancel major version issue 8. CES 9. uber error log enhancement 10. CIS new api 11. trade status issue in cashflow blotter 12. [User Friendly] Bic netting error on historical cashflow after bic netting update + reinstate 13. [User Friendly] [LOANIQ] Should move status to SETTLED after receive 'ACK' msg from downstream 14. [User Friendly] Trade Status displayed as VALD instead of COMP 15. [Dashboard] Pending in Group blotter post manual delivery |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | Refer to releaseWI: [Release 12931708 RATAN BAU Monthly Release - Apr](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12931708) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | Attached to CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 18/04/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 09:00~10:00 |

---

## 2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | Attached to CR |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane Edward* | ADO pipeline |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*