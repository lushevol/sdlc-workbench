Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Zhenzhen Liu @Yunzhe Ta | 2026-01-13 | | | |

### **Description **

- MO requires to build an exception workflow with integrated design to have rules defined/executed on trades going through** cancel and amend **to determine genuineness and associated P&L impact on trades. Objective is to compute real-time PV(present value) impact for any trade in scope undergoing a cancel or amend by computing the PV difference between the new/last trade version and the previous one using T-1 EOD market data. Trades and PVs impacts are subsequently processed by MO with appropriate treatment as per internal policy : [link](https://confluence.global.standardchartered.com/display/FPGWIP/FM+Middle+Office+-+Cancel+and+Amend+Policy) ​C&A are understood as : **Cancellation & Amendment**, Removal of the last market operations (undo). C&A Rogue trading risk committed for remediation in RTP for June 2026. Cancel and Amends (C&A) acknowledgment is a process to review trade booking changes across all Financial Markets products and represents a key control for several very-high gross risk failure points, helping to protect against there being a Fraudulent Derivative Trade (as described in the FM Operational Risk Framework).

| Phase | Scope |
| --- | --- |
| MVP1 | The MVP1 is limited to **FMRP Blade trades** SOURCE_SYSTEM=**SABRE** The MVP1 is limited to **FMRP China Linear Rates desk** BUSINESS_HIERARCHYL1=|Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|Rates|EM Rates|EM Rates - Greater China |
| MVP2 | MVP1 is focusing on PV related check only, MVP2 is to enhance the current design to support more processors, including pv check, non-pv check, no-reportable check etc. Meanwhile, when design new structure, considering code reusage, flexibility, scalability etc - **Non PV**: Enable 9 new C&A checking rules in Ratan to fulfil MVP2 scope business requirement. - Extend the capability to support more entities, from MVP1 (only CN supported) scope to all FMRP scope booking entities. |

### **Main Flow Diagram **

![](https://confluence.global.standardchartered.com/download/attachments/3501535281/cancel%20and%20amend.png?api=v2)

MVP2 basic flow chart

![image-2026-1-13_16-52-2.png](attachments/image-2026-1-13_16-52-2.png)

| <u>**MRB: SIDR V1**</u>**:** Sabre MRB, RG Finance - MRB to generate the T0 PV data three times a day. 03:00 P.M. SGT, GMT and UST - SABRE to sent new sub trade level PV feeds to RATAN EOD with effective time stamp. |
| --- |
| **<u>RATAN EOD</u>: ** - Consume new feed files from Sabre for CnA T0 PV. - Create a new view in One Valuation View (OVV) and expose the API for consumers (RATAN ONE. DQSL) |
| **<u>DQSL</u>: ** - Setup new view for CnA T0 PV. |
| **<u>RATAN ONE</u>: ** - Source trade data from TDS3. - Make calls to RATAN EOD API for getting the PV data. - Stich the data using join conditions, and apply the necessary filters & aggregation. - Apply the Middle Office control rules (7 of them). - Produce the output for end users - as **RATAN ONE UI or download report?** - **Any user action within RATAN ONE ?? ** |

### PV Data Feed

Sabre to feed 3 batches of PV data to Ratan per day. Below are Feed receiving timing at RATAN One and OLA.

| | **Expected Timing Sabre ****Feed to OVV** | **Expected Timing Ratan to generate exceptions** |
| --- | --- | --- |
| **Batch 1** | T 03:00 PM SGT (6:00AM UTC) | T 04:00 PM SGT (7:00AM UTC) |
| **Batch 2** | T 03:00 PM UKT (2:00PM UTC) | T 04:00 PM UKT (3:00PM UTC) |
| **Batch 3** | T 03:00 PM UST (6:00PM UTC) | T 04:00 PM UST (7:00PM UTC) |
| **Batch EOD** | T+1 00:00AM UTC | T+1 01:00AM UTC to get the previous version trade's PV - The PV from this EOD file is for Ratan to get the previous version trade's PV when calculate PV impact |

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | ratanone_ca_control_service.ca_trade | Short description for job |
| 2 | ratanone_ca_control_service.ca_control_job | |
| 3 | ratanone_ca_control_service.ratan_scheduler_shdlck | |
| 4 | select * from ratan_exception_platform.rep_exception where business_flow = 'CANCEL_AND_AMENDMENT' and description like '%NO PV%'; | check C&A PV exception |

### **Jobs**

List the function related jobs and description

| # | Job Name | Description |
| --- | --- | --- |
| 1 | Job name | Short description for job |
| 2 | | |

### **Topic/queue/service related **

List the function related topic queue service and description

| # | Name | Description |
| --- | --- | --- |
| 1 | name | topic to receive OVV notification |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| Tool name | Short description |

### **Issue**

- List the related issue links or you can insert "Content by Label" macro, then all KB with same label would show here

### **Related articles **

- [Ratan Trade Control Onboarding - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Ratan+Trade+Control+Onboarding)
- [C&A Exceptions MVP2 Tech Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3502315523)
- [C&A Exceptions (MVP2) -Requirements - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3015035563)
- [C&A Exception Blotter Feature && User Case - FM Strategy and Planning - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3385440935)
- [C&A User Guideline - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3560744076)