# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** Ratan
**Application Name:** Ratan
**Change Request ID:** CHG0999254
**Date:** 20/06/2026
**DEV Owner/Lead:** Nick
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | RATAN ONE ISO Release for 4A & Hybrid Address |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Story 13852040 [ISO] 2026 4a Go-Live - CN, EG, KE, ZA, TZ](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13852040) [Story 12336525 [ISO] Hybrid Address Enhancement in Swift generation](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12336525) [Story 13708682 BCS: Remove the validation that account number must be 20 digits and Alphanumeric](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13708682) [Story 10138505 Enable camt.057 & camt.058 for Central Bank Egypt](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10138505) [Story 14349075 [ISO] Field-72 enhancement in Pre-MX-Translator for SCBLTH Entity](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14349075) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | 1. ISO 4a release - CN, EG, KE, ZA, TZ 2. ISO Hybrid Address Enhancement in Swift generation 3. Remove the validation that account number must be 20 digits and Alphanumeric 4. Enable camt.057 & camt.058 for Central Bank Egypt 5. Field-72 enhancement in Pre-MX-Translator for SCBLTH Entity |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [Release 14104679 RATAN ISO Release for 4A & Hybrid Address](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14104679) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | Attached to CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 20/06/2026 |
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