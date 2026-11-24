Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| | | | | |

### **

Description **

- Marker checker process to be involved for exceptional handling. multi cases would trigger the exceptions 0 Pending trade confirmation/affirmation:, exception can be closed automatically once confirmation/affirmation is received 1 SSI stamping 2 High value check 3 NSTP rules : One of the Ratan One settlement orchestration work flow tasks, this task will load the pre-defiend NSTP rules( Static data maintained in individual service) and proceed the cash flow SCBML against the NSTP rules.NSTP rule will work as a black list, when the cash flow SCBML meet the NSTP rule Ratan would hold this cash flow SCBML. Then user can manual review the NSTP cashflow in cashflow blotter and generate the swift message per requirement. 4 Back Value check 5 Net /Settled as gross 6 .....

### **Main Flow Diagram **

Add flow diagram and related description for user easy understanding

### **![](https://confluence.global.standardchartered.com/download/attachments/2660629748/Excetpion%20flow.png?api=v2)**

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | Job name | Short description for job |
| 2 | | |

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
| 1 | name | Short description |
| 2 | | |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| Tool name | Short description |

### **Issue**

- List the related issue links or you can insert "Content by Label" macro, then all KB with same label would show here
- -**-trade confirmation status check ** select trade_id as "Trade_Id", trade_version as "Trade_Version", tracking_version as "Tracking_Version", confirmation_status as "Confirmation.Confirmation_Message_Inbound_Status", fmrp_confirmation_status as "Confirmation.Confirmation_Status", confirmation_outbound_status as "Confirmation.Confirmation_Message_Outbound_Status", near_leg_confirmation_status as "Confirmation.Near_Leg_Confirmation_Status", far_leg_confirmation_status as "Confirmation.Far_Leg_Confirmation_Status" from ratanone.ratan_trade__trade where ( trade_id = '4934592') **--Below status means trade has been confirmed** - Inbound Completed - Match Completed - Inbound Completed - Inbound Not Required - Inbound Completed - Match Outside CDU

### **Related articles **

- [High Value Exception Scenario Analysis - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/High+Value+Exception+Scenario+Analysis)
- [Multi Exceptions - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Multi+Exceptions)