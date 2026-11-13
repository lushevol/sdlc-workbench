# ** **

## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Bug 15748974 Central monitoring: latency metrics missing](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15748974) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | Bug Fix : t5 might arrives earlier than t2 and when computing t5 - t2, there is no t2 found for t5. |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | [Test Plan 15763830 Test Plan for 15700464 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=15763830&suiteId=15763836) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) | [Test Plan 15763830 Test Plan for 15700464 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=15763830&suiteId=15763836) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) | [Test Plan 15763830 Test Plan for 15700464 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=15763830&suiteId=15763836) |
| - UAT Sign-off (Link or Attachment, Comment if NA) | [Release 15700464 RATANONE central monitoring- 29th Aug 2026](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15700464) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | [Test Plan 15763830 Test Plan for 15700464 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=15763830&suiteId=15763836) |
| **Implement Plan** | - Attestation if any manual steps | [Release On 2026-08-29 CR: CHG1056852 RATAN Central Monitoring - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-08-29+CR%3A+CHG1056852+RATAN+Central+Monitoring) |
| **UVT plan** | - List details of UVT plan for each story | [Release On 2026-08-29 CR: CHG1056852 RATAN Central Monitoring - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-08-29+CR%3A+CHG1056852+RATAN+Central+Monitoring) |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | [Release On 2026-08-29 CR: CHG1056852 RATAN Central Monitoring - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-08-29+CR%3A+CHG1056852+RATAN+Central+Monitoring) |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 29/08/2026 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | 2 hours |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | Safe |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | NA |
| - PSS Core Function confluence page - PSS Interface confluence page | No change |
| **Monitor** | - Attestation if any monitoring need add or update | No change |