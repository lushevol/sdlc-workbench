**Project Name:** Ratan
**Application Name:** Ratan
**Change Request ID:** CHG1006731
**Date:** 13/06/2026
**Owner/Lead:** Geoffrey
**PSS Manager:** Jane

## A-1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) | Application/Maintenance |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | [Release 14315682 CHG1006731: Korea OLTP UVT](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14315682) |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Story 13719470 [FMRP 8.0] Production Uber to be tested in test envrionment](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13719470) [Story 11839497 [Korea]Integration for OLTP via Solace Korea](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11839497) |
| **Justification** | - [ ] Provide details of involved **infra changes**. | |
| **Justification Attachment** | - [ ] **Non-prod test result** attached. - [ ] **Sign-off** attached. | 1） Add an Uber target flow and the corresponding flow filter configuration to the message-bridge's database to obtain SG Uber messages and prepare for SG data analysis 2）Ratan needs to perform UVT testing with Korea OLTP, sending only two Kafka messages |
| **Implementation Plan Attachment** | - [ ] **AIG (Automation Implementation Guide)** attached. - [ ] **AIG Test Sign-off** attached (test results included). - [ ] *Note: Only AIG attached here will be referred for implementation.* | Attached to CR |
| **Affected CIs** | - [ ] Confirm the list is correct (related servers, upstream/downstream). | RATAN |
| **Change Scheduling** | - [ ] Change window covers **UVT and Rollback** actions. - [ ] Any downtime outside **Greenzone** has **BO's Approval** (Attached to Justification). | 13/06/2026 |
| **PSS Resource Booking** | - [ ] PSS resource booked (if required). - [ ] Duration: **2 hours maximum** per CR (including implementation & verification). | 09:00~10:00 |

---

## A-2. AIG (Automation Implementation Guide)

*Ensure the implementation plan is automated, verified, and follows standards.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **AIG Main Sections** | The AIG must include the below main sections: - [ ] **a. Deployment details** - [ ] **b. UVT Verification** - [ ] **c. Rollback Plan** | |
| **Deployment Method** | - [ ] **ADO pipeline is the only option** for the deployment. - [ ] *Anything else needs dispensation approval from Gevin/Jane/Edward.* | |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **Project Manager** | | | |
| **Technical Lead** | | | |
| **PSS Manager** | | | |
| **Change Manager** | | | |