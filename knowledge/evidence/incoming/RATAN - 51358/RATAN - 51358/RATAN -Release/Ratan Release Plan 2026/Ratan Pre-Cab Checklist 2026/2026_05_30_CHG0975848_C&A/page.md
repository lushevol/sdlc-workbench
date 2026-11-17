# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** RATAN
**Application Name:** RATAN
**Change Request ID:** CHG0975848
**Date:** 30/05/2026
**DEV Owner/Lead: **Wayne
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | Ratan C&A rule enhancement release |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Release 13120892 RATANONE C&A Release - 30th May 2026](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13120892/) [Story 12155275: C&A Enhance rule Non-Std. Counterparty - Boards](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12155275) [Story 12155291: C&A Enhance rule Repeated Amendments on same Counterparty (High) - Boards](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12155291) [Story 12155301: C&A Enhance rule Repeated Amendments on same Trade ID (High) - Boards](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12155301) [Story 12877660 First Layer filter To exclude high volume of expiry and trade events](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12877660) [Story 13426848 Inclusion of root cause for Post maturity rule in C&A exception closure](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13426848) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | refer to [CHG0975848 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3D504b267b3b54c79879674064c3e45a1c%26sysparm_domain%3Dnull%26sysparm_domain_scope%3Dnull%26sysparm_view%3D) for further details |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [CnA Release-202605 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/2519fd84-d406-455a-b7a1-a7dcb0327762/) [Release On 2026-05-30 CR:CHG0975848 C&A](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3685664425) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | In CR: [CHG0975848 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3D504b267b3b54c79879674064c3e45a1c%26sysparm_domain%3Dnull%26sysparm_domain_scope%3Dnull%26sysparm_view%3D) |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 30/05/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 9:00 ~11:00 |

---

## 2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | In CR: [CHG0975848 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3D504b267b3b54c79879674064c3e45a1c%26sysparm_domain%3Dnull%26sysparm_domain_scope%3Dnull%26sysparm_view%3D) |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane Edward* | In ADO |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*