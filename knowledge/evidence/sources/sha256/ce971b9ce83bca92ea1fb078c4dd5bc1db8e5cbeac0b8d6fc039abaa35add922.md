# **

**

## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Release 16587573 CHG1090309: RATAN Settlement 26C feature](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16587573) [Story 14449450 [FMRP 9.0 Commodities Priority] Precious Metals - Swift Msg - Field_26_Commodity_Identity](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14449450) [Story 15351030 [RATAN Settlement Foundation] Extend CES usage to Group Blotter](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15351030) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | 1、Enhance existing precious metal flow for uber message a. Swift 26C generation b. Netting for precious metal fields c. precious metal fields query for downstreams [UBER Precious Metals Tech Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/UBER+Precious+Metals+Tech+Design) 2、Extend CES usage to Group Blotter + Dashboard last 3 cards |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | [Release 16587573 CHG1090309: RATAN Settlement 26C feature](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16587573) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) |
| - UAT Sign-off (Link or Attachment, Comment if NA) | [Test Case 16627608 [Acceptance Testing] UAT sign off for 26c](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16627608) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | NA |
| **Implement Plan** | - Attestation if any manual steps | All ADO pipelines |
| **UVT plan** | - List details of UVT plan for each story | |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | All ADO pipelines |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 10/10/2026 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | 19:00~07:00 |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | SAFE |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | NA |
| - PSS Core Function confluence page - PSS Interface confluence page | NA |
| **Monitor** | - Attestation if any monitoring need add or update | NA |