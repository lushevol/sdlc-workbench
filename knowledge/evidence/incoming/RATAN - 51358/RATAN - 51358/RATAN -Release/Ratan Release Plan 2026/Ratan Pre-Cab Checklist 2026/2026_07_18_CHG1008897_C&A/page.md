# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** RATAN
**Application Name:** RATAN
**Change Request ID:** CHG1008897
**Date:** 18/07/2026
**DEV Owner/Lead: **Wayne
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | Ratan C&A rule enhancement release CHG1008897 |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Release 14390796 RATANONE C&A Release - 18th July 2026](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14390796) [Story 13667609](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13667609): Build connection between TDS3 and Ratan for Sabre Native trade |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | refer to [CHG1008897 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3D0005c0bf3b5d8b9c0d825d0b16e45af1%26sysparm_domain%3Dnull%26sysparm_domain_scope%3Dnull%26sysparm_view%3D) for further details |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [CnA Release-202607-0 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/9f588a8e-3bc9-4f5a-8da3-92b45a58adeb/) [Release On 2026-07-18 CR: CHG1008897 C&A - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3768460248) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | In CR: [CHG1008897 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3D0005c0bf3b5d8b9c0d825d0b16e45af1%26sysparm_domain%3Dnull%26sysparm_domain_scope%3Dnull%26sysparm_view%3D) **Note** 1 CTASK assigned to EDMI team for new solace queue creation: [CTASK2151450](https://scbnow01.service-now.com/change_task.do?sys_id=3145c4373b9d8b9c0d825d0b16e45a2b&sysparm_record_target=change_task&sysparm_record_row=2&sysparm_record_rows=3&sysparm_record_list=change_request%3D0005c0bf3b5d8b9c0d825d0b16e45af1%5EORDERBYnumber) 1 CTASK assigned to SABRE team for replaying trades: [CTASK2194094](https://scbnow01.service-now.com/change_task.do?sys_id=ee188b613b06431471017364c3e45a7c&sysparm_record_target=change_task&sysparm_record_row=3&sysparm_record_rows=3&sysparm_record_list=change_request%3D0005c0bf3b5d8b9c0d825d0b16e45af1%5EORDERBYnumber) |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN, SABRE, SOLACE |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 18/07/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 18:00 ~29:00 (SGT) [CTASK2151449](https://scbnow01.service-now.com/change_task.do?sys_id=394584373b9d8b9c0d825d0b16e45a09&sysparm_record_target=change_task&sysparm_record_row=1&sysparm_record_rows=3&sysparm_record_list=change_request%3D0005c0bf3b5d8b9c0d825d0b16e45af1%5EORDERBYnumber) |

---

## 2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | In CR: [CHG1008897 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3D0005c0bf3b5d8b9c0d825d0b16e45af1%26sysparm_domain%3Dnull%26sysparm_domain_scope%3Dnull%26sysparm_view%3D) |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane Edward* | In ADO |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*