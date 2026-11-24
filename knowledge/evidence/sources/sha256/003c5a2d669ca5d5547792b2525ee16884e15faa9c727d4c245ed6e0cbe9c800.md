# **

**

## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Feature 11351709 [Business Feature] Enable Settlement for Manual Entities (12 EBBS entities)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11351709) [Story 15973009 Enable FULL STP for required inter entity netting rule](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15973009) [Story 15955532 [Last Mile Check] Backend swift MX header hotfix](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15955532) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | 1.Manual entity tranche 2 release 2.Enable FULL STP for required inter entity netting rule 3.[Last Mile Check] Backend swift MX header hotfix |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | ![image-2026-9-2_12-14-26.png](attachments/image-2026-9-2_12-14-26.png) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) |
| - UAT Sign-off (Link or Attachment, Comment if NA) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | |
| **Implement Plan** | - Attestation if any manual steps | All ADO pipelines |
| **UVT plan** | - List details of UVT plan for each story | |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | All ADO pipelines |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 05/09/2026 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | 09:00~10:00 |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | SAFE |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | NA |
| - PSS Core Function confluence page - PSS Interface confluence page | NA |
| **Monitor** | - Attestation if any monitoring need add or update | NA |