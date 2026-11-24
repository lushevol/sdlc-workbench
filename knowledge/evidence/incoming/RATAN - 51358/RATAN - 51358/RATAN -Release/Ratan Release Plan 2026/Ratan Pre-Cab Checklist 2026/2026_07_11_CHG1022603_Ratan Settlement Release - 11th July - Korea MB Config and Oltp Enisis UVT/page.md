## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Release 14760869 CHG1022603: Korea MQ config and OLTP/Enisis UVT](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14760869) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | 1，send ENISIS MX/MT messages and send OLTP pay/receive messages for UVT 2，Change the Enisis MX message format to XML 3，create 3 connection for Korea MQ KOREAMXG.RATAN.TRD.RQSTIN / RATAN.KOREAMXG.FLW.RESP/ KOREAMXG.RATAN.TRD.RQSTIN |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | [Pipelines - Run 20260707.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13374888&view=sc-ado.sc-release-extension-prod.test-report-tab) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) | [Pipelines - Run 20260707.10](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13374888&view=sc-ado.sc-release-extension-prod.test-report-tab) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) | NA |
| - UAT Sign-off (Link or Attachment, Comment if NA) | |
| - DR Test Evidence (Link or Attachment, Comment if NA) | NA |
| **Implement Plan** | - Attestation if any manual steps | [Release 14760869 CHG1022603: Korea MQ config and OLTP/Enisis UVT](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14760869) |
| **UVT plan** | - List details of UVT plan for each story | in install plan |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | pipeline rollback |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 12th July 19:00 ~ 13th July 07:00 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | true |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | Safe |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | true |
| - PSS Core Function confluence page - PSS Interface confluence page | true |
| **Monitor** | - Attestation if any monitoring need add or update | NA |

![image-2026-7-3_14-34-26.png](attachments/image-2026-7-3_14-34-26.png)