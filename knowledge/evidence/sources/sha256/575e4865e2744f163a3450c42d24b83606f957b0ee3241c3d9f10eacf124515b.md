# **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

**Project Name:** RATAN
**Application Name:** RATAn
**Change Request ID:** CHG0955479
**Date:** 18/4/2026
**DEV Owner/Lead:** Jay
**PSS :** Jane

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) <u>[Change Category & Subcategory](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289)</u> | Application/Upgrade |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | RATAN Trade Control Monthly Release - Apr |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Release On 2026-04-18 CR: CHG0955479 Trade Control - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-04-18+CR%3A+CHG0955479+Trade+Control) 11415578: [Technical] RATAN - FMRPSTELLA - Booking API Upgrade for Trade Validation 11598525: [Trade Control] Bug fix for Story 9839686 - Detective Rule23 across multiple trades | Maturity Mismatch for trades under same Structure ID 11737715 Floating LNBRs - Trade ticket and payment schedule update 11741931 Onboard Step_Quantity_Of_Underlier fields into Trade Blotter 11913078 [RATAN Trade Control]As a MO user, I want to onboard product FRA(Forward Rate Agreement) into Trade Blotter 12086131 ASEAN_160 - TC - other cashflow - the format of holiday column is wrong 12334196 [Technical] Cashflow Query API change 12499753 Rule - Cannot hit rule 'CDS Start & End date Equal' 12500297 RATAN should send business event to Stella during Manual validation 12529868 Complex rule - RATAN rule to create - variable notional for com swaps 12699856 [Bug] Missing Fixing Source in Ratan 12711436 Q126 Enhancement - Detective Rule across multiple trades: Maturity Mismatch for trades under same Structure ID 12975129 TC - ASEAN CPT issue no 13&15- Trade Detail & Version Compare - the value of 'Additional Party Payment Amount' should be split by , 13090938 [Bug] Premium amount in Ratan mismatch against Murex |
| **Justification** | - [ ] **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - [ ] **Issue Fixing:** Provide the issue nature and fix details. | [Release-2026Apr - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/f6e6bc40-c0e2-4b4f-a5cb-79cd47bdc2c0/) [Release 12878457 RATANONE Trade Review Release - 18th Apr 2026](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12878457) |
| **Justification Attachment** | The following materials must be attached: - [ ] **a. RCA:** Root Cause Analysis (for issue fixing). - [ ] **b. Change Test Sign-off:** 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). DR Test Evidence - [ ] **c. BPMS_Pre-CAB_Checklist** (with SME sign-off). - [ ] **d. UAT Sign-off** (Required for functional changes). | Technical 1. Stella Booking API Upgrade for Trade Validation 2. Cashflow Query API change Enhancement 1. Detective Rule across multiple trades: Maturity Mismatch for trades under same Structure ID 2. Floating LNBRs - Trade ticket and payment schedule update 3. Onboard Step_Quantity_Of_Underlier fields into Trade Blotter 4. Onboard product FRA(Forward Rate Agreement) into Trade Blotter 5. Send business event to Stella during Manual validation 6. Complex rule - RATAN rule to create - variable notional for com swaps Bug Fix 1. The format of holiday column is wrong, need fix display 2. Rule 'CDS Start & End date Equal' , parse JSON from a single value to list 3. Missing Fixing Source. 4. Trade Detail & Version Compare - the value of 'Additional Party Payment Amount' should be split by 5. Premium amount in Ratan mismatch against Murex |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | In CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window should cover UVT and Rollback actions. - [ ] Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 18/4/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - [ ] Duration: **2 hours maximum** for each CR (including both implementation and verification). | 9:00 ~10:00 |

---

## 2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | In CR |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane Edward* | |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*