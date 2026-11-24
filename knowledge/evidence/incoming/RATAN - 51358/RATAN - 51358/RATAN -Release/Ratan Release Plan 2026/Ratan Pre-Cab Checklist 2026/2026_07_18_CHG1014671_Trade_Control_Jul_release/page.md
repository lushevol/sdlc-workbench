## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | Application/Upgrade |
| **Justification** | - **Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - **Issue Fixing:** Provide the issue nature, fix details | [Release-2026Jul - Boards](https://dev.azure.com/sc-ado/FMQPR/_queries/query/e94eb7bd-7f0f-47ed-8053-1dc71c4d8c45/) **FXO enhance :** 9839601 - [FXO] FX replication enhancement to exclude DCD/FX_DCD/FX_PCD 14147454 - [FXO] Enhance Trade Ticket for VanillaOption, NDO, Barrier, Digital **Credit :** 12662879 - [Credit] onboarding CDS/CDI template trade ticket into trade blotter 13054148 - [Credit] onboarding CDS/CDI template Payment Schedule 13817329 - [Credit] CDS/CDI: Rename the field name in Ratan & Remove fields in Ratan 13817353 - [Credit] CDS/CDI: Add Coupon Direction in Trade Ticket **Common enhance:** 13442239 - Date Format Change in Ratan to align with Blade and email source - Phase 1 13722964 - Trade Search - Remove default Source System during the trade query 13737508 - Add BTB fields into Trade Blotter/Exception Blotter 13755820 - [Technical] Upgrade and Use New RATAN Foundation Version 14208598 - Add new fields and update display logic for InterestRate:LoanDeposit 14234420 - Ratan Trade View Confirmation - Implementation **Bug fix:** 14181730 - TC - Should hide comparison window after opening new blotter 14203160 - TC - Send wrong params to request when selected Filter 14488470 - [Trade Control] FXO - Unable to view full decimal in View Contract |
| **Test Evidence** ** **** ** | - Functional Test Evidence (Link or Attachment, Comment if NA) | ![image-2026-7-14_10-14-31.png](attachments/image-2026-7-14_10-14-31.png) |
| - Regression Test Evidence (Link or Attachment, Comment if NA) | |
| - Performance Test Evidence (Link or Attachment, Comment if NA) | |
| - UAT Sign-off (Link or Attachment, Comment if NA) | |
| - DR Test Evidence (Link or Attachment, Comment if NA) | |
| **Implement Plan** | - Attestation if any manual steps | In CR |
| **UVT plan** | - List details of UVT plan for each story | [Release On 2026-07-18 CR: CHG1014671 Trade Control - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-07-18+CR%3A+CHG1014671+Trade+Control) |
| **Rollback plan** | - List details of rollback plan <Reject if any manual steps> | In CR |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 18/07/2026 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | 18/07/2026 9:00 ~11:00 |
| **Safe Change Attestations** | - Attestation status and Results Safe Change Dashboard [https://fmtools.global.standardchartered.com/safe-change-dashboard/](https://fmtools.global.standardchartered.com/safe-change-dashboard/) - Approval from CRP Meeting(Thursday) if result as Non-Compliant | |
| **Document update** ** ** | - OLA - SLA - ASRM - DOI | |
| - PSS Core Function confluence page - PSS Interface confluence page | |
| **Monitor** | - Attestation if any monitoring need add or update | |