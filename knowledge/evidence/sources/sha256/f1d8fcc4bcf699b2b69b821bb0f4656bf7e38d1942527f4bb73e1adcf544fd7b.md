# ** 

**

## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Story 14758676 [Archival & Retrieval] production technical live phase 2](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14758676/) [Story 12176942 Development of Auto DVP Function](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12176942) [Story 15865347 Tag53 customization for VNO SBV](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15865347) [Story 15876211 F72 customization in MX for VN](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15876211) [Story 15096696 [Enhancement] Enhance cashflow history comment when techFail](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15096696) [Generic Task 15251731 [PSS Production Query Support] ITRS alert : Failed to obtain JDBC Connection](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15251731) [Story 16178894 Enable FULL STP for Inter Entity Netting SG vs UK](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16178894) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | 1.Data archive phase2 2.Auto DVP release 3.Manual entity biz live 4.Tag53 customization for VNO SBV 5.F72 customization in MX for VN 6.[Enhancement] Enhance cashflow history comment when techFail 7.[PSS Production Query Support] ITRS alert : Failed to obtain JDBC Connection 8.Enable FULL STP for Inter Entity Netting SG vs UK |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | ![image-2026-9-16_17-8-4.png](attachments/image-2026-9-16_17-8-4.png) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) |
| - UAT Sign-off (Link or Attachment, Comment if NA) | [https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14930303&view=sc-ado.sc-release-extension-prod.test-report-tab](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14930303&view=sc-ado.sc-release-extension-prod.test-report-tab) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | |
| **Implement Plan** | - Attestation if any manual steps | All ADO pipelines |
| **UVT plan** | - List details of UVT plan for each story | |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | All ADO pipelines |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 19/09/2026 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | 09:00~10:00 |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | SAFE |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | |
| - PSS Core Function confluence page - PSS Interface confluence page | |
| **Monitor** | - Attestation if any monitoring need add or update | |