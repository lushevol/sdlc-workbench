## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Story 15506023 Enhancement for non-eco amend check for migrated data](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15506023) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | Enhancement for non-eco amend check for migrated data |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | [Pipelines - Run 20260808.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14122620&view=sc-ado.sc-release-extension-prod.test-report-tab) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) | [Pipelines - Run 20260808.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14122620&view=sc-ado.sc-release-extension-prod.test-report-tab) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) | NA |
| - UAT Sign-off (Link or Attachment, Comment if NA) | |
| - DR Test Evidence (Link or Attachment, Comment if NA) | NA |
| **Implement Plan** | - Attestation if any manual steps | [Release 15506020 RATAN Settlement Enhancement for non-eco amend check for migrated data -CHG1050584](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15506020) |
| **UVT plan** | - List details of UVT plan for each story | dummy trade under the wiki below "UVT Step" |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | pipeline rollback |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 10th Aug 10:00 PM ~ 11th Aug 09:00 AM |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | Safe |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | OLA PSS sign-off |
| - PSS Core Function confluence page - PSS Interface confluence page | |
| **Monitor** | - Attestation if any monitoring need add or update | NA |