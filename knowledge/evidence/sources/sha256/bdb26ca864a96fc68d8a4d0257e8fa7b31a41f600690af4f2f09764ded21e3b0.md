# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** RATAN
**Application Name:** RATAN
**Change Request ID:** CHG0993226
**Date:** 04/07/2026
**DEV Owner/Lead: **Wayne
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | Ratan C&A rule enhancement release |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Release 12589053 RATANONE C&A Release - 4th Jul 2026](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12589053/) [Story 12143665](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12143665): Strategic Enhancements - Trade Data Standardization [Story 12160164](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12160164): Strategic Enhancements - Bond PV calculation engine [Story 12498586](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12498586): CnA scope TP system topic separation [Story 13661934](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13661934): First Layer of Exclusion for Razor trades [Story 13665574](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13665574): Generic Business events exclusion list for Current Version [Story 13780786](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13780786): Remove white list check for C&A Non-PV [Story 13864095](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13864095): First Layer of Exclusion for Sabre Native trades [Story 13895993](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13895993): Enable Uber json for C&Asa [Story 14028465](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14028465): First Layer of Exclusion for Blade trades [Story 14207295](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14207295): Update generic First Layer Exclusion list refet to the comments under [RATAN-Trade Control: C&A Exception - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3582658499&refresh=1782472163875&focusedCommentId=3750225534&refresh=1782472177655#comment-3750225534) for the change of Kafka |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | refer to [CHG0993226 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3Dac7c959c3bc5cf90f6935d0b16e45a3b) for further details |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [CnA Release-202606 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/da938d2a-5b68-4f92-8ec4-da475fbf9ba2/) [Release On 2026-07-04 CR: CHG0993226 C&A - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3651563702) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | In CR: [CHG0993226 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3Dac7c959c3bc5cf90f6935d0b16e45a3b) |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 04/07/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 9:00 ~11:00 |

---

## 2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | In CR: [CHG0993226 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3Dac7c959c3bc5cf90f6935d0b16e45a3b) |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane Edward* | In ADO |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*