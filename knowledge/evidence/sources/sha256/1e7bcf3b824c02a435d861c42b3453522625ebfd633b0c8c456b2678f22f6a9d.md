# **

**

## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Story 14864946 Adjust the number of queues to receive RTA messages from all countries](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14864946) [Generic Task 14759533 [DevOps] Solace Self-Service Pipeline Release](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14759533) [Story 14593614 [enhancement] optimize the performance of cashflow provider api(Heap memory)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14593614) [Story 14871966 [BAU Enhancement] no economic amendment logic enhancement for group service](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14871966) [Story 14734906 Inter Entity Netting - add new counterparty mapping - TAIPEI](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14734906) [Story 14828884 Inter Entity Netting - add new counterparty mapping - LDN](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14828884) [Story 14891048 [BUGFIX] Parent cashflow wrong status when withdrawal comes after child cashflow settled](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14891048) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | 1.Adjust the number of queues to receive RTA messages from all countries 2.Solace Self-Service Pipeline release to production 3.Optimize the performance of cashflow provider API 4.No economic amendment logic enhancement for group service 5.Inter Entity Netting - add new counterparty mapping for TAIPEI, LDN 6.Parent cashflow wrong status when withdrawal comes after child cashflow settled 7. Enlarge Topic Cash_Settlement_Auto_DVP_Receive partition to 6 8. HCV rotate 9. Manual entity UVT for BH |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | ![image-2026-7-15_11-26-4.png](attachments/image-2026-7-15_11-26-4.png) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) |
| - UAT Sign-off (Link or Attachment, Comment if NA) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | |
| **Implement Plan** | - Attestation if any manual steps | Attached to CR |
| **UVT plan** | - List details of UVT plan for each story | |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | ADO pipeline rollback |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 18/07/2026 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | 09:00~10:00 |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | SAFE |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | |
| - PSS Core Function confluence page - PSS Interface confluence page | |
| **Monitor** | - Attestation if any monitoring need add or update | NA |