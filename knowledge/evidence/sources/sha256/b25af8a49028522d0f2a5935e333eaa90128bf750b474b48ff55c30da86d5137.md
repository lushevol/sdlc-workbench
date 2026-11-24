# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** Ratan
**Application Name:** Ratan
**Change Request ID:** 
**Date:** 30/05/2026
**DEV Owner/Lead:** Geoffrey
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | 1. fxu phase2 ： 1. Pastdue 2. Reversal 3. Partial Util 4. Settlement Method Update 2. Korea FM Solace UVT 3. EBBS accounting jobs are removed from control-m |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Story 11396537 FXU - Ratan Cash Settlement - Strategic phase 2](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11396537) [Story 11922468 [UBER merge] [Regression Cover] optimize accounting EBBS job --- phase2](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11922468/?view=edit) [Story 13666667 Korea Solace integration UVT](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13666667) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | 1. Partial Utilization (Utilize partial amount of cashflow original amount) 1. When: as long as utilization amount is not full original cashflow amount, then it would be partial 2. Accounting model for 'Partial Util' cashflows - CR Bridge Account 40 & DR FXBRREC Account 40: Utilization amount(Partial) **- 1st Partial Util** - CR Bridge Account 60 & DR PastDue Account 60: remaining amount**- EOD pastdue ****Util** - Cashflow Status - **PARTIALLY-UTILIZED + PastDue** - CR PastDue 60 & DR Bridge Account 60: reverse the remaining amount **- reverse pastdue ****Util - No reverse request from FXU** - CR Bridge Account 20 & DR FXBRREC Account 20: Utilization amount(Partial) **- 2nd Partial Util - util request from FXU** - Cashflow Status -** PARTIALLY-UTILIZED + PastDue ** - CR Bridge Account 30 & DR FXBRREC Account 30: Utilization amount(Partial) **- 3rd Partial Util - util request from FXU** - CR Bridge Account 10 & DR PastDue Account 10: remaining amount**- EOD pastdue ****Util** - Cashflow Status -** PARTIALLY-UTILIZED + PastDue** 3. Only on contract level 2. PastDue Utilization (To cancel the previous Full or Partial Utilization event) 1. When: Configurable by different entity, no requirement by counterparty/currency. Timing to be confirmed by Rajesh. 2. Who: VD today or back value date cashflow. 3. Accounting model for 'Pastdue Util' cashflows - CR Bridge Account & DR PastDue Account: remaining amount( Full) **- on VD** - **Cashflow Status - PASTDUE + PastDue ** - DR Bridge Account & CR PastDue Account: Revere the remaining amount **- post VD Pastdue full/ Partial Util** - CR Bridge Account & DR FXBRREC Account: Utilization amount(Full) - **Cashflow Status - UTILIZED** 4. If cashflow has passed cutoff on VD, cashflow sub status should be always Pastdue, until it's full utilized (cashflow status = UTILIZED) 5. Only on contract level 6. Pastdue cashflow, a field aging should be showing the time length between current time and VD. 7. add Pastdue into sub status drop down 8. enable remaining amount in cashflow API opened to DQSL/SSDR 9. For cashflow status =Pastdue cashflow, if cashflow is cancelled, then reversed accounting entry will be generated. 3. Reverse Utilization 1. When: either partial/full to be reversed. 2. Accounting model for 'Reverse Util' cashflows - CR Bridge Account & DR FXBRREC Account: Utilization amount( Full or Partial) - DR Bridge Account & CR FXBRREC Account: Revere of utilization, remaining amount has to be added 3. Only on contract level 4. need to support and test on reversal of auto utilization (auto utilization report is not required in FXU) 4. Early Utilization Can support early utilization, same as full/partial/reverse utilization, while accounting will be sent on SOD VD |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [Release 11876451 CHG0923574： RATAN Settlement FXU Phase 2 Go-Live](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11876451) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | Attached to CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 30/05/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 09:00~11:00 |

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