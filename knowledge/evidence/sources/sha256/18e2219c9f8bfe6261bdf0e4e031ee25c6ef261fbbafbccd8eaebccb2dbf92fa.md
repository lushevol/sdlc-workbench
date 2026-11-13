# **MO1 ****2026_07_25_CHG1021940_Change Short Description 

**

## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | Application/upgrade |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | **CDUPS**: [Story 15014945 [MO1] CDUPS Nginx Change](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15014945) From the DR requirements, the container host will be removed, all ui static goes to one host. **ENTRA**: [Story 15015075 [MO1] Entra SSO house keeping](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15015075) 1. clean up cache flags for Entra migration period to prevent abuse of feature flags. 2. add tracking logs for Entra usage. |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | [https://dev.azure.com/sc-ado/FMQPR/_TestManagement/Runs?runId=10291585&_a=resultSummary&resultId=100000](https://dev.azure.com/sc-ado/FMQPR/_TestManagement/Runs?runId=10291585&_a=resultSummary&resultId=100000) ![image-2026-7-22_12-0-19.png](attachments/image-2026-7-22_12-0-19.png) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) | [https://dev.azure.com/sc-ado/FMQPR/_testManagement/runs?runId=10295356&_a=runSummary](https://dev.azure.com/sc-ado/FMQPR/_testManagement/runs?runId=10295356&_a=runSummary) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) | NA |
| - UAT Sign-off (Link or Attachment, Comment if NA) | CDUPS Signoff [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15014945#19493340](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15014945#19493340) FSS Signoff [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15014893#19498325](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15014893#19498325) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | NA |
| **Implement Plan** | - Attestation if any manual steps | ADO pipeline |
| **UVT plan** | - List details of UVT plan for each story | refer to [Release On 2026-07-25 CR:CHG1021940 Markets Operations One](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-07-25+CR%3ACHG1021940+Markets+Operations+One) UVT Plan |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | ADO rollback |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | NA |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | Done |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | NA |
| - PSS Core Function confluence page - PSS Interface confluence page | NA |
| **Monitor** | - Attestation if any monitoring need add or update | NA |