# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** RATAN
**Application Name:** RATAN
**Change Request ID:** CHG0991246
**Date:** 13/06/2026
**DEV Owner/Lead:** Zhou, Jay
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | application/upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | RATAN Trade Control Monthly Release - Jun |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Release On 2026-06-13 CR: CHG0991246 Trade Control - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-06-13+CR%3A+CHG0991246+Trade+Control) |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | [Release-2026Jun - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/ec03d0e7-dc86-409c-99b3-7d8ab5d43ddd/) |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | **Trade Ticket/UI:** 7461950 - UI Enhancement for multi leg FXO and validation for whole Contract 10088881 - display trades netting results for FXO 11510326 - View Contract to be added under Trade Blotter 11886843 - Implement FXO Contract Validation Design and Enhanced Add Comment Handling 11965200 - Enhance Trade Ticket for Barrier, Double Barrier, Digital, Barrier Digital, and Double Barrier Digital Products 12189506 - Trade Blotter: Onboard Touch product with template in Trade Details 12205563 - Display historical netted trade in "History" 12351516 - [Trade Control] Enhancement for Story 9885389 - History in Trade Blotter 12442354 - New entities onboarding FXO (including G10/india) 12750899 - Enhance Trade Ticket for Vanilla, NDO, Barrier, Double Barrier, Digital, Barrier Digital, and Double Barrier Digital Products (2) 13129615 - User able to copy the counterparty FM ID from the search panel 13442127 - Query and integrate "FMCODE" into "Additional Payment" table & "Other Cashflows" 13514464 - Comments should appear in MO Exception blotter front display 13717640 - Enhance FX Barrier field display logic - Barrier Style 13799885 - "View Contract" UI enhancement 13808986 - Adjust logical field of compounding calc for IR CCS/Swap 14004361- [Trade Control] Discontinue of ECONFAFFIRMED workflow in FMRP - Remove "ECON AFFIRMED" from Validation Status in Ratan **FX replication rule:** 9839601 - [FXO] FX replication enhancement to exclude DCD/FX_DCD/FX_PCD 12893473 - FX replication for new event: RemainingPartyPartial/StepOutFull/StepOutPartial **Enhancement: ** 11372548 - Netting Trade Validation 12913457 - onboard new fields to fiter/view/Rule Blotter for Credit 13091199 - Onboarding new fields for G10 in RATAN 13661211 - Enhance Trade Ticket for FX Barrier and Digital 13755820 - Upgrade Foundation to Version 7.1.3 (Spring Boot 4.0.6) **Bug Fix:** 13383014 - [Bug] Missing dropdown description for payment holiday using "View Contract" 13528578 - TC - payment schedule - Shouldn't display cashflow that event type is 'withdrawal' in payment schedule 13542952 - [Bug] Incorrect validation static when using MO comment 13559974 - TC - Fields should be remove for ForeignExchange:SimpleExotic:Barrier Product_Sub_Type: Double Barrier 13561784 - TC- Missing value in Contract comparison 13688887 - [Bug Trade - Control] Coupon captured in Other Cashflow 13896489 - TC - Missing 'settlement date' field for Touch product Settlement 13719470 - [FMRP 8.0] Production Uber to be tested in test envrionment 11839497 - Integration for OLTP via Solace Korea |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | In CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 13/06/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 2 hours |

---

## 2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane Edward* | |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*