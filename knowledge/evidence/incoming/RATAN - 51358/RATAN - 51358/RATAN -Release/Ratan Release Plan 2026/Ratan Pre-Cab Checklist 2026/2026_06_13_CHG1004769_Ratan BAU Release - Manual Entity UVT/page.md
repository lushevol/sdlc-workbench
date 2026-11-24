# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** Ratan
**Application Name:** Ratan
**Change Request ID:** CHG1004769
**Date:** 13/06/2026
**DEV Owner/Lead:** Nick
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Maintenance |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | Manual Entity EBBS Connectivity Verify - LK/GH |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Story 14242334 Manual entity fourth batch UVT - LK, GH](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14242334) [Story 14241935 [enhancement] optimize the performance of cashflows provider API (SSDR timeout issue)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14241935) [Story 14246856 [enhancement] rule engine thread safe defect that lead cashflow to be tech fail](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14246856) [Story 14296781 [enhancement] payment schedule query to apply parent trade version](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14296781) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | Manual entity connectivity UVT - LK, GH Optimize the performance of cashflows provider API (SSDR timeout issue) Rule engine thread safe defect that lead cashflow to be tech fail Apply trade version when calling TDSX to query payment schedule |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [Release 14236794 RATAN BAU Release - Manual Entity EBBS Connectivity Verify - LK/GH](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14236794) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | Attached to CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 13/06/2026 |
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