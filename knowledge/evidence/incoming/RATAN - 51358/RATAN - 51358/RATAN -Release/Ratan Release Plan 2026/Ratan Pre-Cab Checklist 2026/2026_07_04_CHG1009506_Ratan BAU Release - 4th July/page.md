# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** Ratan
**Application Name:** Ratan
**Change Request ID:** CHG1009506
**Date:** 04/07/2026
**DEV Owner/Lead:** Nick
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | RATAN BAU Release - 4th July |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Story 14059589 [BAU Enhancement] MT/MX related fields special characters handling](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14059589) [Story 13191219 [RATANONE BAU]Cashflow Blotter FM address switch to registered address](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13191219) [Story 11920456 [RATANONE BAU]Cashflow Details: Move to Direct GraphQL for Safer Reuse](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11920456) [Story 13423003 [Ssi-service Enhancement] adjust consume ssi+ refresh event logic](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13423003) [Story 14604092 Auto DVP tech golive, optimize logic and log](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14604092) [Story 14649115 [enhancement] Fix duplicate payment issue for component and resultant cashflow](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14649115) [Story 14683450 Manual entity sixth batch UVT - TZ](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14683450) [Story 14711448 Connectivity testing to for JP](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14711448) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | 1.MT/MX related fields special characters handling 2.Cashflow Blotter FM address switch to registered address 3.Cashflow Details: Move to Direct GraphQL for Safer Reuse 4.ssi-service enhancement to adjust consume ssi+ refresh event logic 5.Auto DVP optimize logic and log 6.Fix duplicate payment issue for component and resultant cashflow 7.Manual entity UVT - TZ 8.EBBS Connectivity testing for JP |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [Release 14406979 RATAN BAU Release - 4th July](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14406979) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | Attached to CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 04/07/2026 |
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