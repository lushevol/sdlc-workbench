## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Story 12372052 [FMRP Day 2] Solace Queue Refactoring & split based on Taxonomies](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12372052) [Story 14172910 [FMRP Day 2] Split Kafka Topic (tdsx_uber_message_json_inbound) into 7 by Taxonomies and Enhancement on uber msg consuming](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14172910) |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | 1，mb create flows for uber split queue 2，group receives uber messages from split topic |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | [solace queue split test case for Uber - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/solace+queue+split+test+case+for+Uber) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) | [Pipelines - Run 20260720.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13656091&view=sc-ado.sc-release-extension-prod.test-report-tab) |
| - Performance Test Evidence (Link or Attachment, Comment if NA) | [MB][solace queue split PT for Uber - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/solace+queue+split+PT+for+Uber) [[group] PT of consuming messages on multiple Uber topics - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/%5Bgroup%5D+PT+of+consuming+messages+on+multiple+Uber+topics) |
| - UAT Sign-off (Link or Attachment, Comment if NA) | [solace queue split test case for Uber - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/solace+queue+split+test+case+for+Uber) |
| - DR Test Evidence (Link or Attachment, Comment if NA) | NA |
| **Implement Plan** | - Attestation if any manual steps | [Release 14641062 CHG1018358: RATAN Settlement FMRP Day2 Split queue](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14641062) |
| **UVT plan** | - List details of UVT plan for each story | dummy trade under the wiki below "UVT Step" [Release On 2026-07-25 CR: CHG1018358 FMRP Day2 Split queue - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-07-25+CR%3A+CHG1018358++FMRP+Day2+Split+queue) |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | pipeline rollback |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 25th July 17:00 PM ~ 26th July 05:00 AM |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | Safe |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | OLA PSS sign-off |
| - PSS Core Function confluence page - PSS Interface confluence page | |
| **Monitor** | - Attestation if any monitoring need add or update | NA |