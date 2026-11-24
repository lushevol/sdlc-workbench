**Project Name:** Ratan
**Application Name:** Ratan
**Change Request ID:** CHG0999429
**Date:** 13/06/2026
**Owner/Lead:** Nick
**PSS Manager:** Jane

## A-1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Category** | - [ ] Category and Subcategory based on change nature and activities. - [ ] Refer to: [Change Category Guide](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3518175289) | Application/Maintenance |
| **Short Description** | - [ ] Must be meaningful and accurate. - [ ] Include brief description of this change. | [Release 14107146 RATAN Kafka Cluster Upgrade](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14107146) |
| **Description** | - [ ] The related ADO work item/story must be stated here. | [Story 14105237 Kafka Cluster Upgrade on Production](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14105237) |
| **Justification** | - [ ] Provide details of involved **infra changes**. | [Release 14107146 RATAN Kafka Cluster Upgrade](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14107146) |
| **Justification Attachment** | - [ ] **Non-prod test result** attached. - [ ] **Sign-off** attached. | RATAN Kafka cluster upgrade to v3.8.0 |
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