# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** RATAN
**Application Name:** RATAN
**Change Request ID:** CHG1026932
**Date:** 25/07/2026
**DEV Owner/Lead: **Wayne
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | Ratan C&A rule enhancement release CHG1026932 |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Release 14869392 RATANONE C&A Release - 25th July 2026](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14869392/) [Story 12509017](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12509017): Strategic Enhancements - Generic exception handling [Story 13661997](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13661997): Rule enhance - NON-Reportable Rule for Razor trades [Story 13662204](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13662204): Rule enhance - External to Internal Amendment (High) [Story 13662281](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13662281): Rule enhance - Non-Std. Portfolio (High) [Story 13662841](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13662841): Blade: To identify previous version for non-PV and non-reportable rules [Story 13662996](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13662996): Razor: To identify previous version for non-PV and non-reportable rules [Story 13665188](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13665188): Razor - Repeated Amendments on same Counterparty [Story 13665271](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13665271): Exceptional case handling due to upstream data quality issue [Story 13863256](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13863256): Razor - Repeated Amendments on same Trade ID (High) [Story 13864760](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13864760): Rule enhance - Back or Future-Dated C&A (High) for Sabre Native trades [Story 13865013](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13865013): Rule enhance - Post Maturity Date (High) for Sabre Native trades [Story 13865115](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13865115): Repeated Amendments on same Counterparty for Sabre Native [Story 13865309](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13865309): Repeated Amendments on same trade Id for Sabre Native [Story 13865660](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13865660): Saber Native: To identify previous version for non-PV and non-reportable rules [Story 14923202](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14923202): Consume split Uber topics [Story 14929968](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14929968): Rollback Falcon APIs [Story 15128493](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15128493): Saber Native: To update first layer of exclusion (identify current version) for non-PV and non-reportable rules |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | refer to [CHG1026932 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3De57b92403b864f50b8e57364c3e45a86) for further details |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | [CnA Release-202607 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/c3051dc2-4b4b-435d-9c0d-deba47d115eb/) [Release On 2026-07-25 CR: CHG1026932 C&A - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3793696045) Performance comparison before and after adding the indexes: [Query cost time for index update - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Query+cost+time+for+index+update) Regression Test Evidence: [Pipelines - Run 20260721.6](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13701088&view=sc-ado.sc-release-extension-prod.test-report-tab) |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | In CR: [CHG1026932 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3De57b92403b864f50b8e57364c3e45a86) |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 25/07/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 17:00(SAT) ~05:00(SUN) |

---

## 2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | In CR: [CHG1026932 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3De57b92403b864f50b8e57364c3e45a86) |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane Edward* | In ADO |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*