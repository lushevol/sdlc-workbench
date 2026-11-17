## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | Application/Upgrade |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | [TCUP release-202609-1 - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/f6cf659f-162c-48a6-b155-21d4cce9b684/) [Release 14725299 RATANONE TCUP Release - 19th Sep 2026 - Load More](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14725299) [CHG1048194 | Change Request | SC](https://scbnow01.service-now.com/now/nav/ui/classic/params/target/change_request.do%3Fsys_id%3D7d4ac6452ba60f58ad51f95fee91bfe5%26sysparm_view%3D%26sysparm_domain%3Dnull%26sysparm_domain_scope%3Dnull) [Release On 2026-09-19 CR: CHG1048194 TCUP-Load More - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-09-19+CR%3A+CHG1048194+TCUP-Load+More) [Story 13838821](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13838821): Exception Blotter: Maximum Records Display & Group By for Bulk Action |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | [Test Plan 14790242 Test Plan for 14725299 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=14790242&suiteId=14790251) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) | [Test Plan 14790242 Test Plan for 14725299 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=14790242&suiteId=14790251) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) | [Test Plan 14790242 Test Plan for 14725299 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=14790242&suiteId=14790251) |
| - UAT Sign-off (Link or Attachment, Comment if NA) | [Release 14725299 RATANONE TCUP Release - 19th Sep 2026 - Load More](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14725299) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | [Test Plan 14790242 Test Plan for 14725299 - Test Plans](https://dev.azure.com/sc-ado/FMQPR/_testPlans/execute?planId=14790242&suiteId=14790251) |
| **Implement Plan** | - Attestation if any manual steps | All ADO pipelines |
| **UVT plan** | - List details of UVT plan for each story | [13838821] |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | All ADO pipelines |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 19/09/2026 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | 09:00~11:00 |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | SAFE |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | NA |
| - PSS Core Function confluence page - PSS Interface confluence page | NA |
| **Monitor** | - Attestation if any monitoring need add or update | NA |