# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** RATAN
**Application Name:** RATAN
**Change Request ID:** CHG0970268
**Date:** 23/05/2026
**DEV Owner/Lead:** Jay
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | application/upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | RATAN Trade Control Monthly Release - Apr |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Release On 2026-05-23 CR: CHG0970268 Trade Control - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-05-23+CR%3A+CHG0970268+Trade+Control) [Story 13054003 Add Leverage & Compounding Calc in Ratan Trade Details - Trade Ticket](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13054003) [Story 13128345 Add Declearing into default Business event list](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13128345) [Story 13190503 [Trade Control] [Technical] [Process Enhancement] Close exceptions in bulk in Exception Platform](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13190503) [Bug 13323029 Exception is not auto-closed](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13323029) [Story 13444098 [Trade Control] Detective Rule23 across multiple trades | Maturity Mismatch for trades under same Structure ID - group by packa...](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13444098) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | [Release-2026May - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/385df33e-8bc0-455b-a468-504c2a02675e/) [Release 13281796 RATANONE Trade Review Release - 23th May 2026](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13281796) |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | Trade Ticket: Add Leverage & Compounding Calc in Ratan Trade Details Add Declearing into default Business event list Enhancement: Close exceptions in bulk in Exception Platform Detective Rule23: across multiple trades | Maturity Mismatch for trades under same Structure ID - group by package Bug fix: trade can't be dropped from exception rule as expected Test plan: [Test Plan 13770918 Test Plan for 13281796 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=13770918&suiteId=13813606) Regression test: [Pipelines - Run 20260515.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12259234&view=sc-ado.sc-release-extension-prod.test-report-tab) ![image-2026-5-20_11-4-26.png](attachments/image-2026-5-20_11-4-26.png) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | In CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 23/05/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 9:00 ~ 11:00 |

---

## 2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | In CR |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane Edward* | In ADO |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*