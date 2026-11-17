# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** Ratan
**Application Name:** Ratan
**Change Request ID:** CHG0974600
**Date:** 23/05/2026
**DEV Owner/Lead:** Nick
**PSS : **Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | RATAN BAU Monthly Release - 23rd May |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Story 11759077 RFI Nostro stamping based on Portfolio Dev - Nostro query customization](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11759077) [Story 11759088 [Cross Border Debit MT103 & 202] MT202 dev](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11759088/) [Bug 4734047 [BAU][Nostro Static] Export window will not show quick search on nostro static](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/4734047/) [Story 12967234 Rebook exception](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12967234) [Story 13826606 Manual entity second batch UVT](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13826606) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | 1.RFI Nostro stamping based on Portfolio - Nostro query customization 2.Cross Border Debit MT103 & 202 3.Nostro Static, Nostro Export component UI style enhancement 4.Rebook exception - change rebook tagging logic from within 10 days to 5 days with same trade id 5. manual entity EBBS connectivity testing for VN, ZM, UG |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [Release 13400478 RATAN BAU Monthly Release - 23rd May](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13400478) [Release On 2026-05-23 CR: CHG0974600 BAU - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-05-23+CR%3A+CHG0974600+BAU) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | Attached to CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 23/05/2026 |
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